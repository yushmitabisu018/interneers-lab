from django.urls import path
from week3.controllers import product_controller

urlpatterns = [
    path("products", product_controller.products_api),
    path("products/<str:product_id>", product_controller.products_detail_api)
]