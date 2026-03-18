from django.db import models
from mongoengine import Document, StringField, FloatField, IntField,DateTimeField
import datetime
# Create your models here.

class Product(Document):
     name = StringField(required=True)
     description = StringField()
     category = StringField()
     brand = StringField()
     price = FloatField(required=True)
     quantity = IntField(required=True)
    
     created_at = DateTimeField(default=datetime.datetime.utcnow)
     updated_at = DateTimeField(default=datetime.datetime.utcnow)

     def to_dict(self):
        data = self.to_mongo().to_dict()
        data["id"] = str(data["_id"])
        del data["_id"]
        return data