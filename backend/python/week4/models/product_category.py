from mongoengine import Document, StringField, DateTimeField
from datetime import datetime, timezone

class ProductCategory(Document):
    title =StringField(required=True, unique=True)
    description= StringField()

    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'product_categories'
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        if not self.created_at:
            self.created_at = self.updated_at
        return super().save(*args, **kwargs)

    def to_dict(self):
       return {
           "id": str(self.id),
           "title": self.title,
           "description": self.description
       }