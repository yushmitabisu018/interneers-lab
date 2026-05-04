from ..models import ProductCategory
from datetime import datetime, timezone

class ProductCategoryRepository:    
    @staticmethod
    def create_category(title, desc=None):
        category = ProductCategory(
            title=title,
            description = desc
        )
        category.save()
        return category
    
    @staticmethod
    def get_all_categories():
        return ProductCategory.objects()
    
    @staticmethod
    def get_category(cat_id):
        return ProductCategory.objects(id=cat_id).first()

    @staticmethod
    def update_category(cat_id, update_data):
        allowed_updates = {"title", "description"}
        category = ProductCategory.objects(id=cat_id).first()

        if not category:
            return None
        
        for key, value in update_data.items():
            if key in allowed_updates:
                setattr(category, key, value)
        
        category.updated_at= datetime.now(timezone.utc)
        category.save()
        return category

    @staticmethod    
    def del_category(cat_id):
        category = ProductCategory.objects(id=cat_id).first()
        if not category:
            return False
        
        category.delete()
        return True