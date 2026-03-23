from django.apps import AppConfig


class Week4Config(AppConfig):
    name = 'week4'
   
    def ready(self):
        from week4.scripts.seed import seed_categories
        seed_categories()
