from ..repositories.product_category_repository import ProductCategoryRepository
from ..repositories.product_repository import ProductRepository

class ProductCategoryService:
    @staticmethod
    def create_category(data):
        title = data.get("title")
        description = data.get("description")

        if not title:
            raise ValueError("Title is required")
        
        return ProductCategoryRepository.create_category(title, description)
    
    @staticmethod
    def get_all_categories():
        return ProductCategoryRepository.get_all_categories()
    
   
    @staticmethod
    def get_category(cat_id):
        return ProductCategoryRepository.get_category(cat_id)
    
    @staticmethod
    def update_category(cat_id, update_data):
        category = ProductCategoryRepository.get_category(cat_id)

        if not category:
            raise ValueError("Category not found")
        
        return ProductCategoryRepository.update_category(cat_id, update_data)
     

    @staticmethod
    def delete_category(cat_id):
        value = ProductCategoryRepository.del_category(cat_id)

        if not value:
            raise ValueError("Category not found")
        
        return True
    
    @staticmethod
    def get_products_by_category(cat_id):
        category = ProductCategoryRepository.get_category(cat_id)

        if not category:
            raise ValueError("Category not found")

        return ProductRepository.filter_products({
            "categories": [str(category.id)]
        }) 
    
    @staticmethod
    def add_product_to_category(cat_id, product_id):
        category = ProductCategoryRepository.get_category(cat_id)

        if not category:
            raise ValueError("Category not found")
        
        product = ProductRepository.get_product(product_id)
        if not product:
            raise ValueError("Product not found")
        
        return ProductRepository.add_category(product, category)
    
    @staticmethod
    def remove_product_from_category(cat_id, product_id):
        category = ProductCategoryRepository.get_category(cat_id)

        if not category:
            raise ValueError("Category not found")
        
        product = ProductRepository.get_product(product_id)
        if not product:
            raise ValueError("Product not found")
        
        return ProductRepository.remove_category(product, category)
    
