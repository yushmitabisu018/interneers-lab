from ..models import Product
import datetime
from bson import ObjectId
from bson.errors import InvalidId

class ProductRepository:
    def create(self,data):
        product = Product(**data)
        product.save()
        return product    
    
    def get_all(self):
        return Product.objects()
    
    def get_product(self, product_id):
        return Product.objects(id=product_id).first()  

    allowed_updates= {"name","price","quantity","description"}

    def update_product(self, product_id,update_data):
        try:
           obj_id = ObjectId(product_id)
        except (InvalidId, TypeError):
          return None
        
        product = Product.objects(id=obj_id).first()
        if not product:
            return None
        
        for key,value in update_data.items():
           if key in self.allowed_updates: 
            setattr(product,key,value)

        product.updated_at =datetime.datetime.now(datetime.timezone.utc)
        product.save()
        
        return product
        
    def delete_product(self, product_id):
        product = Product.objects(id=product_id).first()
        if not product:
          return False
      
        product.delete()
        return True
