from mongoengine import Document, DateTimeField, StringField, FloatField, ListField, ReferenceField
from datetime import datetime
from .product_category import ProductCategory

class Product(Document):
    name = StringField(required=True)
    brand = StringField(required=True)   
    price = FloatField(min_value=0)

    categories = ListField(ReferenceField(ProductCategory))  #many to many

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'products'
    }

    def to_dict(self):
      return {
        "id": str(self.id),
        "name": self.name,
        "brand": self.brand,
        "price": self.price,
        "categories": [str(c.id) for c in self.categories]
    }