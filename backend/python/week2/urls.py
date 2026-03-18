from django.urls import path
from . import views

urlpatterns =[
   path('products', views.products_view),
   path('products/<int:product_id>', views.product_detail_view),    
]