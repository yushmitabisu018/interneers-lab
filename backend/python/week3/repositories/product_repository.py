from ..models import Product
import datetime
from bson import ObjectId

class ProductRepository:
    def create(self,data):
        product = Product(**data)
        product.save()
        return product    
    
    def get_all(self):
        return Product.objects()
    
    def get_product(self, product_id):
        return Product.objects(id=ObjectId(product_id)).first()
    
    def update_product(self, product_id,update_data):
        product = Product.objects(id=ObjectId(product_id)).first()
        if not product:
            return None
        
        for key,value in update_data.items():
            setattr(product,key,value)

        product.updated_at = datetime.datetime.utcnow 
        product.save()
        
        return product
        
    def delete_product(self, product_id):
      product = Product.objects(id=ObjectId(product_id)).first()
      if not product:
       return False
      
      product.delete()
      return True
