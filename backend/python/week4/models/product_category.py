from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class ProductCategory(Document):
    title =StringField(required=True, unique=True)
    description= StringField()

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'product_categories'
    }

    def to_dict(self):
     return {
        "id": str(self.id),
        "title": self.title,
        "description": self.description
    }