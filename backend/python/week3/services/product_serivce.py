from ..repositories.product_repository import ProductRepository

#business logic
class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def create_product(self,data):
     return self.repository.create(data)
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_product(self,product_id):
       return self.repository.get_product(product_id)
    
    def update_product(self, product_id, update_data):
       return self.repository.update_product(product_id, update_data)
    
    def delete_product(self,product_id):
       return self.repository.delete_product(product_id)