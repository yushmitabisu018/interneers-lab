from django.urls import path
from .controllers import product_controller, category_controller

urlpatterns =[
    path('categories/', category_controller.categories_api),
    path('categories/<str:category_id>/', category_controller.categories_detail_api),
     
    path('categories/<str:category_id>/products/', category_controller.category_products_api),
    path('categories/<str:category_id>/products/<str:product_id>/', category_controller.category_product_detail_api),
    
     path('products/bulk-upload/', product_controller.bulk_upload_products),
     path('products/', product_controller.products_api),
     path('products/<str:product_id>/', product_controller.product_detail_api),

]