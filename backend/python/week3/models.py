from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
from datetime import datetime, timezone
# Create your models here.

class Product(Document):
    name = StringField(required=True)
    description = StringField()
    category = StringField()
    brand = StringField()
    price = FloatField(required=True)
    quantity = IntField(required=True)
    
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(timezone.utc)
        if not self.created_at:
            self.created_at = self.updated_at
        return super().save(*args, **kwargs)
    
    def to_dict(self):
        data = self.to_mongo().to_dict()
        data["id"] = str(data["_id"])
        del data["_id"]
        return data