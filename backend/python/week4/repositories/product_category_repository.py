from ..models import ProductCategory

class ProductCategoryRepository:    
    @staticmethod
    def create_category(title, desc=None):
        catgory = ProductCategory(
            title=title,
            description = desc
        )
        catgory.save()
        return catgory
    
    @staticmethod
    def get_all_categories():
        return ProductCategory.objects()
    
    @staticmethod
    def get_category(cat_id):
        return ProductCategory.objects(id=cat_id).first()
    
    @staticmethod
    def update_category(cat_id, update_data):
        category = ProductCategory.objects(id=cat_id).first()

        if not category:
            return None
        
        for key,value in update_data.items():
          setattr(category,key,value)

        category.save()
        return category

    @staticmethod    
    def del_category(cat_id):
        category = ProductCategory.objects(id=cat_id).first()
        if not category:
            return False
        
        category.delete()
        return True