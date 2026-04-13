import sys
import os

# to add backend/python to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from week5.db import init_db
from week4.services.product_service import ProductService
from week4.services.product_category_service import ProductCategoryService

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
from google import genai
import json

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.subheader("AI scenario generator")
scenario= st.selectbox(
   "Choose scenario",
   ["Normal", "Holiday Rush", "Clearance Sale"]
)

def get_prompt(scenario):
    if scenario=="Holiday Rush":
        return """
        Generate exact 10 toy products with HIGH stock(quantity between 100 and 500).
        Return ONLY a valid JSON array.
        Each object must have:
        name, brand, price, quantity
        """

    elif scenario== "Clearance Sale":
        return """
        Generate exact 10 toy products with LOW stock(quantity between 1 and 20).
        Return ONLY a valid JSON array.
        Each object must have:
        name, brand, price, quantity
        """

    else:
        return """
        Generate exact 10 toy products with NORMAL stock(quantity between 20 and 100).
        Return ONLY a valid JSON array.
        Each object must have:
        name, brand, price, quantity
        """

def gen_ai_products(prompt):
   response= client.models.generate_content(
      model= "gemini-2.5-flash-lite",
      contents=prompt
   )    
   return response.candidates[0].content.parts[0].text

def parse_products(text):
    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        json_text = text[start:end]

        return json.loads(json_text)

    except Exception as e:
        st.error(f"JSON parsing failed: {e}")
        # st.write("Raw output:", text)
        return []

def save_products(products):
    try:
        ProductService.create_product({
           "name": p["name"],
            "brand": p["brand"],
            "price": float(p["price"]),
            "quantity": int(p["quantity"]),
            "categories": [] 
        })
    except Exception as e:
        st.error(f"Failed to save product: {str(e)}")

if st.button("Generate Scenario Data"):
    with st.spinner("Generating AI data..."):
        prompt = get_prompt(scenario)
        raw_text = gen_ai_products(prompt)
        products = parse_products(raw_text)

        if products:
            save_products(products)
            st.success(f"{len(products)} products added!")
            st.write(products[:10])