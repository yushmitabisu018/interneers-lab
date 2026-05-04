from django.apps import AppConfig
from django_app.db import init_db

class Week3Config(AppConfig):
    name = 'week3'
    
    def ready(self):
        from mongoengine.connection import get_connection #to prevent running multiple times
        try:
            get_connection() 
        except Exception:    
            init_db()