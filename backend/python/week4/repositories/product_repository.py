import logging
from ..models import Product, ProductCategory
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ProductRepository:
    @staticmethod
    def create_product(data):
        product = Product(**data)
        product.save()
        return product
    
    @staticmethod
    def get_product(product_id):
        return Product.objects(id=product_id).first()
    
    @staticmethod
    def update_product(product_id, data):
        allowed_updates = {"name", "brand", "price", "quantity", "categories"}
        product = Product.objects(id=product_id).first()
        if not product:
            return None

        for key, value in data.items():
           if key in allowed_updates: 
            setattr(product, key, value)

        product.updated_at= datetime.now(timezone.utc)
        product.save()
        return product
    
    @staticmethod
    def del_product(product_id):
        product = Product.objects(id=product_id).first()

        if not product:
            return False
        
        product.delete()
        return True
    
    @staticmethod
    def add_category(product,category):
        if category not in product.categories:
            product.categories.append(category)
            product.save()
            
        return product

    @staticmethod    
    def remove_category(product,category):
        if category in product.categories:
            product.categories.remove(category)
            product.save()

        return product    
    
    @staticmethod
    def filter_products(filters:dict):
        query ={}

        categories = filters.get("categories")
        if categories and len(categories)>0:
            try:
                category_objs = ProductCategory.objects(id__in=categories)
                query["categories__in"] = list(category_objs)
            except Exception as e:
                logger.exception("Invalid category filter passed to filter_products")
                raise ValueError("Invalid category IDs provided") from e

        if filters.get("price_min") is not None:
            query["price__gte"] = filters["price_min"]

        if filters.get("price_max") is not None:
            query["price__lte"] = filters["price_max"]        
        
        if filters.get("brand"):
            query["brand"] = filters["brand"]

        products = Product.objects(**query)


        sort = filters.get("sort")
        allowed_sorts = {"price", "-price", "name", "-name"}
        if sort:
            if sort not in allowed_sorts:
                raise ValueError("Invalid sort parameter")
            products = products.order_by(sort)
        
        page = int(filters.get("page",1))
        limit = int(filters.get("limit",10))
        skip = (page-1)*limit
        
        products = products.skip(skip).limit(limit)

        return products


