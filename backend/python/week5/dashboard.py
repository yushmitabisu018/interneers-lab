import sys
import os
import shutil

# to add backend/python to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

from google import genai
import json

from week5.db import init_db
from week4.services.product_service import ProductService
from week4.services.product_category_service import ProductCategoryService
from week6.utils import clean_and_parse_json
from week6.schemas import ProductSchema
from week7.utils import cosine_similarity
from week8.utils.document_loader import load_documents
from week8.utils.chunking import split_documents
from week8.utils.embeddings import get_embedding_model
from week8.services.vector_store import create_vector_store 
from week8.services.retrieval import retrieve_relevant_chunks
from week8.services.hybrid_rag import generate_hybrid_answer

@st.cache_resource
def init_cached_db():
 init_db()

init_cached_db()

@st.cache_data
def load_products():
    return ProductService.get_products({"page":1, "limit":1000})

all_products = load_products()

@st.cache_resource 
def load_model(): 
    return SentenceTransformer('all-MiniLM-L6-v2') 

model= load_model()

@st.cache_data
def load_products():
    return ProductService.get_products({"page": 1, "limit": 1000})

all_products = load_products()

SEMANTIC_TOP_K = 5 
WEEK8_DIR= os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "week8"))
WEEK8_CHROMA_DIR= os.path.join(WEEK8_DIR, "chroma_db")

RAG_EVAL_CASES = [
    {"query": "What is the return policy?", "expected_source": "return_policy.txt"},
    {"query": "How to use the toy car?", "expected_source": "product_manual.txt"},
    {"query": "How are vendor payments processed?", "expected_source": "vendor_faq.txt"},
]

def knowledge_base_ready():
    return os.path.isdir(WEEK8_CHROMA_DIR) and any(os.scandir(WEEK8_CHROMA_DIR))

@st.cache_data(show_spinner=False)
def build_knowledge_base(force_rebuild=False):
    if force_rebuild and os.path.isdir(WEEK8_CHROMA_DIR):
        shutil.rmtree(WEEK8_CHROMA_DIR)

    documents =load_documents()
    chunks =split_documents(documents)
    embedding_model= get_embedding_model()
    create_vector_store(chunks, embedding_model)

    return len(documents), len(chunks)

def run_rag_eval_suite():
    rows= []
    passed= 0

    for test_case in RAG_EVAL_CASES:
        query= test_case["query"]
        expected_source= test_case["expected_source"]

        results= retrieve_relevant_chunks(query, top_k=1)
        predicted_source= results[0].metadata.get("source") if results else "none"
        test_passed= predicted_source== expected_source

        if test_passed:
            passed+=1

        rows.append(
            {
                "Query": query,
                "Expected Source": expected_source,
                "Predicted Source": predicted_source,
                "Result": "PASS" if test_passed else "FAIL",
            }
        )
    return passed, len(RAG_EVAL_CASES), pd.DataFrame(rows)


st.set_page_config(page_title="Inventory Dashboard")
st.title("Inventory Dashboard")

if "page" not in st.session_state:
    st.session_state.page=0 

if "msg" in st.session_state:
    st.success(st.session_state["msg"])
    del st.session_state["msg"]

#category side bar
st.sidebar.header("Filter")
@st.cache_data(ttl=60)
def get_categories():
 return list(ProductCategoryService.get_all_categories())

categories = get_categories()
category_options = ["All"]+[c.title for c in categories]
sel_category = st.sidebar.selectbox("Filter by category", category_options)

if "last_category" not in st.session_state or st.session_state.last_category != sel_category:
    st.session_state.page = 0
    st.session_state.last_category = sel_category


#filtering
def get_cached_products(sel_category, all_products):
  if sel_category=="All":
      return list(all_products)

  else:
     cat = next((c for c in categories if c.title == sel_category), None)
     if cat is None:
      return None
     return list(ProductCategoryService.get_products_by_category(cat.id))

products = get_cached_products(sel_category, all_products)
if products is None:
   st.warning("Selected category does not exist.")
   products=[]


#embeddings
def get_product_embeddings(products):
    texts = tuple(
        f"{p.name} {p.brand} toy product for customers"
        for p in products
    )
    return _embed_product_texts(texts)


@st.cache_data
def _embed_product_texts(texts):
    embeddings = model.encode(texts)
    embeddings = np.array(embeddings)
    if embeddings.ndim == 1:
        embeddings = embeddings[np.newaxis,:]
    return embeddings, texts

# implementation of keyword and semantic search
st.subheader("Search Products")

search_type = st.radio(
    "Choose search type",
    ["Keyword Search", "Semantic Search"]
)

search_query = st.text_input("Enter search query")


#apply search
filtered_products = products

if search_query and products:
    #keyword Search
    if search_type== "Keyword Search":
        query_words =search_query.lower().split()
        filtered_products= [
            p for p in products
            if any(word in (p.name +" "+ p.brand).lower() for word in query_words)
        ]

    # semantic Search
    else:
        product_embeddings,_ = get_product_embeddings(products)
        query_embedding= model.encode([search_query])[0]
        similarities = []
        for i, emb in enumerate(product_embeddings):
            sim = cosine_similarity(query_embedding, emb)
            similarities.append((products[i], sim))

        similarities.sort(key=lambda x: x[1], reverse=True)

        filtered_products = [p for p, _ in similarities]

        st.write("### Top Matches")
        for p, score in similarities[:SEMANTIC_TOP_K]:
            st.write(f"**{p.name}** → {score:.3f}")


if "last_query" not in st.session_state:
    st.session_state.last_query =""

if search_query != st.session_state.last_query:
    st.session_state.page = 0
    st.session_state.last_query= search_query

if search_query and len(filtered_products) == 0:
    st.warning("No products found")


st.subheader("Ask the Expert")

rag_col1, rag_col2= st.columns([1, 1])
with rag_col1:
    if st.button("Build / Refresh Expert Knowledge Base"):
        with st.spinner("Building vector store from week8 data..."):
            doc_count, chunk_count = build_knowledge_base(force_rebuild=True)
        st.success(
            f"Expert knowledge base refreshed with {doc_count} documents and {chunk_count} chunks."
        )

with rag_col2:
    rag_eval_running = st.session_state.get("rag_eval_running", False)
    if st.button("Run RAG Eval Suite", disabled=rag_eval_running):
        st.session_state.rag_eval_running = True
        try:
            if not knowledge_base_ready():
                with st.spinner("Preparing expert knowledge base first..."):
                    build_knowledge_base(force_rebuild=False)

            with st.spinner("Running RAG eval suite..."):
                score, total, eval_df = run_rag_eval_suite()

            st.write(f"RAG Eval Score: {score}/{total}")
            st.dataframe(eval_df, use_container_width=True)
        finally:
            st.session_state.rag_eval_running = False

if "expert_chat_messages" not in st.session_state:
    st.session_state.expert_chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Ask me about returns, manuals, vendor policy or stocks available. "
                "Example: What is the stock level for Toy Doctor Kit?"
            ),
        }
    ]

for msg in st.session_state.expert_chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg["content"].startswith("Available stock for"):
            st.caption("Stock answers come directly from the product catalog, so this response may not have a separate RAG trace.")
        if msg.get("trace_url"):
            st.markdown(f"[View Trace in LangSmith]({msg['trace_url']})")

user_question = st.chat_input("Ask the Expert...")

if user_question:
    st.session_state.expert_chat_messages.append({"role": "user", "content": user_question})

    with st.chat_message("user"):
        st.markdown(user_question)

    if not knowledge_base_ready():
        with st.spinner("Preparing expert knowledge base..."):
            build_knowledge_base(force_rebuild=False)

    answer, trace_url = generate_hybrid_answer(user_question, all_products)

    with st.chat_message("assistant"):
        st.markdown(answer)
        if answer.startswith("Available stock for"):
            st.caption("Stock answers come directly from the product catalog, so this response may not have a separate RAG trace.")
        if trace_url:
           st.markdown(f"[View Trace in LangSmith]({trace_url})")

    st.session_state.expert_chat_messages.append(
        {"role": "assistant", "content": answer, "trace_url": trace_url}
    )


#find similar function 
def find_similar_products(target_product, products, top_k=3, threshold=0.45):
    product_embeddings, _ = get_product_embeddings(products)

    target_index = None
    for i, p in enumerate(products):
        if str(p.id) == str(target_product.id):
            target_index = i
            break

    if target_index is None:
        return []

    target_embedding = product_embeddings[target_index]

    similarities = []
    for i, emb in enumerate(product_embeddings):
        if i==target_index:
            continue

        sim = cosine_similarity(target_embedding, emb)
        if sim>=threshold:
            similarities.append((products[i], sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]

     
   
#add product
st.subheader("Add new product")
name = st.text_input("Product Name")
brand = st.text_input("Brand")
price = st.number_input("Price", min_value=0.00)
quantity = st.number_input("Quantity", min_value=0)

category_titles = [c.title for c in categories]
select_category = st.selectbox("Select Category", category_titles, key="cat_select")

if st.button("Add Product", key="add_btn"):
    if name.strip() and brand.strip():
      try:
        cat_obj = next((c for c in categories if c.title == select_category), None)
        
        if not cat_obj:
           st.error("Selected category does not exist")
        else:   
         ProductService.create_product({
            "name": name.strip(),
            "brand": brand.strip(),
            "quantity": int(quantity),
            "price": float(price),
            "categories": [str(cat_obj.id)]
         })
         st.cache_data.clear()
         st.session_state["msg"]= "Product added successfully"
         st.rerun()

      except Exception as e:
         st.error(f"Failed to add product: {str(e)}")
           
    else:
        st.error("Fill required fields")


#current inventory
st.subheader("Current inventory")
# st.dataframe(df)       

page_size = 5
total_pages = max(1, (len(filtered_products)-1) //page_size + 1)
start = st.session_state.page *page_size
end = start + page_size

paginated_products = filtered_products[start:end] 
for p in paginated_products:

    with st.container():  
        st.markdown("---")

        col1, col2 = st.columns([4, 1])

        #product info
        with col1:
            st.markdown(f"""
            ### {p.name}
            **Brand:** {p.brand}  
            **Price:** ₹{p.price}  
            **Stock:** {p.quantity}
            """)

        # button
        with col2:
            clicked = st.button("Find similar products", key=f"similar_{p.id}")

        # show similar products
        if clicked:
            results= find_similar_products(p, products)

            with st.expander(f"Similar to {p.name}", expanded=True):  

                for sim_p, score in results:
                    st.markdown(
                        f"- **{sim_p.name}** ({sim_p.brand})→`{score:.3f}`"
                    )

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("Previous", disabled=(st.session_state.page == 0)):  
        st.session_state.page -= 1
        st.rerun()

with col3:
    if st.button("Next", disabled=(end >= len(filtered_products))):
        st.session_state.page += 1
        st.rerun()

st.write(f"Page {st.session_state.page + 1} of {total_pages}")


data=[]
for p in paginated_products:
    data.append({
        "Id": str(p.id),
        "Name": p.name,
        "Brand": p.brand,
        "Quantity": p.quantity,
        "Price": p.price
        }) 

df = pd.DataFrame(data)

# remove product
st.subheader("Remove Product")
if not df.empty:
    product_to_delete = st.selectbox(
        "Select product to delete",
        paginated_products,
        key="delete_select",
        format_func=lambda product: product.name,
    )

    if st.button("Delete Product", key="delete_btn"):
       ProductService.delete_product(product_to_delete.id)
       st.cache_data.clear()
       st.session_state["msg"] = "Product removed successfully"
       st.rerun()

else:
    st.info("No product to delete")


# stock alert
threshold= st.sidebar.slider("Low stock threshold",1,100,10)

if st.button("Stock Alerts"):
    st.subheader("Stock alerts")
    low_stock_items = []

    for p in all_products:
        if p.quantity < threshold:
            low_stock_items.append(p)

    if low_stock_items:
        for item in low_stock_items:
            st.error(f"{item.name} is low on stock (Quantity: {item.quantity})")
    else:
        st.success("All products have sufficient stock")


#WEEK6 
#week6 scenario selector
@st.cache_resource
def get_genai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("AI features will not work.")
        return None
    return genai.Client(api_key=api_key)

st.subheader("AI scenario generator")
scenario= st.selectbox(
   "Choose scenario",
   ["Normal", "Holiday Rush", "Clearance Sale"]
)

def get_prompt(scenario):
    scenarios_config = {
        "Holiday Rush": {"stock_level": "HIGH", "quantity_range": "100 and 500"},
        "Clearance Sale": {"stock_level": "LOW", "quantity_range": "1 and 20"},
        "Normal": {"stock_level": "NORMAL", "quantity_range": "20 and 100"}
    }
    
    config = scenarios_config.get(scenario, scenarios_config["Normal"])
    
    return f"""
    Generate exact 10 toy products with {config['stock_level']} stock(quantity between {config['quantity_range']}).
    Return ONLY a valid JSON array.
    Each object must have:
    name, brand, price, quantity
    """

def gen_ai_products(prompt):
   client = get_genai_client()
   if client is None:
       st.error("Cannot generate AI products: Google API key is not configured.")
       return ""
   
   response= client.models.generate_content(
      model= "gemini-2.5-flash-lite",
      contents=prompt
   )    
   return response.candidates[0].content.parts[0].text

def parse_products(text):
    """
    Parse JSON output from LLM using robust cleaning logic.
    Handles markdown fences, single objects, and arrays.
    """
    products = clean_and_parse_json(text)
    if not products:
        st.error("Failed to parse JSON from AI response. Please try again.")
    return products

def save_products(products):
    if not products:
        return {"added": 0, "failed": 0}

    added = 0
    failed = 0
    for i, p in enumerate(products):
        try:
            ProductService.create_product({
                "name": p["name"],
                "brand": p.get("brand", ""),
                "price": float(p.get("price", 0)),
                "quantity": int(p.get("quantity", 0)),
                "categories": []
            })
            added += 1
        except Exception as e:
            failed += 1
            st.error(f"Failed to save product at index {i}: {str(e)}")

    return {"added": added, "failed": failed}

if st.button("Generate Scenario Data"):
    with st.spinner("Generating AI data..."):
        prompt = get_prompt(scenario)
        raw_text = gen_ai_products(prompt)
        products = parse_products(raw_text)

        if products:
            valid_objs = []
            invalid = []
            for i, item in enumerate(products):
                try:
                    validated = ProductSchema(**item)
                    valid_objs.append(validated)
                except Exception as e:
                    invalid.append({"index": i, "error": str(e), "item": item})

            st.info(f"Validation: {len(valid_objs)} valid, {len(invalid)} invalid")

            if valid_objs:
                # Convert validated models to dicts for insertion
                insert_items = [v.dict() for v in valid_objs]
                result = save_products(insert_items)
                st.success(f"Inserted: {result.get('added',0)}; Failed saves: {result.get('failed',0)}")

            if invalid:
                st.error(f"{len(invalid)} items failed validation. See details below.")
                st.write(invalid[:10])
            else:
                st.write([p.dict() for p in valid_objs][:10])