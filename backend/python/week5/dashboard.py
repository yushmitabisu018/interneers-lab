import sys
import os

# to add backend/python to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd

from db import init_db
from week4.models.product import Product
from week4.models.product_category import ProductCategory

init_db()

st.set_page_config(page_title="Inventory Dashboard")
st.title("Inventory Dashboard")

if "msg" in st.session_state:
    st.success(st.session_state["msg"])
    del st.session_state["msg"]

#category side bar
st.sidebar.header("Filter")
categories = ProductCategory.objects()
category_options = ["All"]+[c.title for c in categories]

sel_category = st.sidebar.selectbox("Filter by category", category_options)
 

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
        cat_obj = ProductCategory.objects(title=select_category).first()

        product = Product(
            name=name.strip(),
            brand=brand.strip(),
            quantity=quantity,
            price=price,
            categories=[cat_obj]
        )
        product.save()
        st.session_state["msg"]= "Product added successfully"
        st.rerun()
    else:
        st.error("Fill required fields")

#filtering
if sel_category=="All":
   products = Product.objects()

else:
   cat = ProductCategory.objects(title=sel_category).first()
   products= Product.objects(categories=cat)


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
st.subheader("Current invnentory")
st.dataframe(df)       


# remove product
st.subheader("Remove Product")
if not df.empty:
    id_selected = st.selectbox("Select product to delete", df["Id"], key="delete_select")

    if st.button("Delete Product", key="delete_btn"):
       product= Product.objects(id=id_selected).first()
       if product:
          product.delete()
          st.session_state["msg"] = "Product removed successfully"
          st.rerun()
else:
   st.info("No product to delete")


# stock alert
threshold=10
if st.button("Stock Alerts"):
   st.subheader("Stock alerts")
   low_stock_itmes=[]
   for p in products:
     if p.quantity<threshold:
        low_stock_itmes.append(p)

   if low_stock_itmes:
     for item in low_stock_itmes:
       st.error(f"{item.name} is low on stock (Quantity: {item.quantity})")

   else:
     st.success("All products have sufficient stock")
