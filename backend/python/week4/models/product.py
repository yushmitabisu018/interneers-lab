from mongoengine import Document, DateTimeField, StringField, FloatField, ListField, ReferenceField, IntField
from datetime import datetime, timezone
from .product_category import ProductCategory

class Product(Document):
    name = StringField(required=True)
    brand = StringField(required=True)   
    price = FloatField(min_value=0, required=True)
    quantity = IntField(default=0)
    categories = ListField(ReferenceField(ProductCategory))  #many to many

    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'products'
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        if not self.created_at:
            self.created_at = self.updated_at
        return super().save(*args, **kwargs)

    def to_dict(self):
        categories = []
        for c in self.categories:
            try:
                categories.append(str(c.id))
            except Exception:
                #if category deleted
                pass

        return {
            "id": str(self.id),
            "name": self.name,
            "brand": self.brand,
            "price": self.price,
            "quantity": self.quantity,
            "categories": categories
        }