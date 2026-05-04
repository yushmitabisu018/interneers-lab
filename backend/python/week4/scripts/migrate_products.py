from week4.models import Product

def migrate_products():
    products = Product.objects()
    for p in products:
        if not p.brand:
            p.brand= "Unknown"
        if not p.categories:
            p.categories=[]
        p.save()
    print("Migration completed")