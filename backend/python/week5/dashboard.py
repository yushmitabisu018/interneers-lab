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
