from ..repositories.product_repository import ProductRepository
from ..models import Product
import csv
from io import TextIOWrapper

class ProductService:
    @staticmethod
    def create_product(data):
        name = data.get("name")
        brand = data.get("brand")
        price = data.get("price")

        if not name:
            raise ValueError("Name is required")
        
        if not brand:
            raise ValueError("Brand is required")
        
        if price is not None and price<0:
            raise ValueError("Price must be positive")
        
        product = Product(
            name=name,
            brand=brand,
            price=price
        )

        product.save()
        return product
    
    @staticmethod
    def get_products(filters):
       return ProductRepository.filter_products(filters)
    
    @staticmethod
    def get_product(product_id):
       return ProductRepository.get_product(product_id)
    
    @staticmethod
    def update_product(product_id, update_data):
        product= ProductRepository.get_product(product_id)

        if not product:
            raise ValueError("Product not found")
        
        return ProductRepository.update_product(product_id, update_data)
     
    @staticmethod
    def delete_product(product_id):
        value = ProductRepository.del_product(product_id)

        if not value:
            raise ValueError("Product not found")
        return True
    
    @staticmethod
    def bulk_create_products(file):
        products = []

        file_data = TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.DictReader(file_data)

        for row in reader:
            # try:
              name= row.get("name")
              brand= row.get("brand")
              price= row.get("price")

              if not name or not brand:
                 continue

              price = float(price) if price else None

              if price is not None and price < 0:
                continue

              product = Product(
                 name=name,
                 brand=brand,
                 price=price
                )

              product.save()
              products.append(product)

            # except Exception:
            #     continue

        return products



        
