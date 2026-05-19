import sys
import os

# to add backend/python to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from google import genai
import json

from week5.db import init_db
from week4.services.product_service import ProductService
from week4.services.product_category_service import ProductCategoryService
from week6.utils import clean_and_parse_json
from week6.schemas import ProductSchema

@st.cache_resource
def init_cached_db():
 init_db()

init_cached_db()
st.cache_data.clear()

st.set_page_config(page_title="Inventory Dashboard")
st.title("Inventory Dashboard")

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

#filtering
def get_cached_products(sel_category):
  if sel_category=="All":
    return list(ProductService.get_products({"limit":100}))

  else:
     cat = next((c for c in categories if c.title == sel_category), None)
     if cat is None:
      return None
     return list(ProductCategoryService.get_products_by_category(cat.id))

products = get_cached_products(sel_category)  
if products is None:
   st.warning("Selected category does not exist.")
   products=[]

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
data=[]
for p in products:
    data.append({
        "Id": str(p.id),
        "Name": p.name,
        "Brand": p.brand,
        "Quantity": p.quantity,
        "Price": p.price
        }) 

df = pd.DataFrame(data)
st.subheader("Current inventory")
st.dataframe(df)       


# remove product
st.subheader("Remove Product")
if not df.empty:
    id_selected = st.selectbox("Select product to delete", df["Id"], key="delete_select")

    if st.button("Delete Product", key="delete_btn"):
       ProductService.delete_product(id_selected)
       st.cache_data.clear()
       st.session_state["msg"] = "Product removed successfully"
       st.rerun()

else:
    st.info("No product to delete")


# stock alert
threshold= st.sidebar.slider("Low stock threshold",1,100,10)

if st.button("Stock Alerts"):
   st.subheader("Stock alerts")
   low_stock_items=[]
   for p in products:
     if p.quantity<threshold:
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