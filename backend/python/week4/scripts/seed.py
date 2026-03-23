from ..models import ProductCategory

def seed_categories():
    categories = ["Food", "Electronics", "Clothing"]

    for title in categories:
        if not ProductCategory.objects(title=title):
            ProductCategory(title=title).save()
    print("Seeding done")