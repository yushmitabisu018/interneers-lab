#product logic
products = []
curr_id = 1 

def validate_product(data):

    if not data.get("name"):
        return "Name is required"
    
    if not data.get("description"):
        return "Description is required"
    
    if not data.get("category"):
        return "Category is required"
    if not data.get("brand"):
        return "Brand is required"
    
    price = data.get("price")
    if price is None or price<=0:
        return "Price must be greater than zero"
    
    quantity = data.get("quantity")
    if quantity is None or quantity<0:
        return "Quantity cannot be negative"
    
    return None
    
def create_product(data):

    error = validate_product(data)
    if error:
        return {"error": error}

    global curr_id

    product ={
        "id": curr_id,
        "name": data.get("name"),
        "description": data.get("description"),
        "category": data.get("category"),
        "price": data.get("price"),
        "brand": data.get("brand"),
        "quantity": data.get("quantity"), 
    }
    products.append(product)
    curr_id+=1

    return product

def get_products(page=1, limit=5):
    start = (page-1)*limit
    end = page*limit
    return products[start:end]

def get_product(product_id):
    for product in products:
        if(product["id"]==product_id):
            return product
        return None
    
def update_product(product_id,data):

     error = validate_product(data)
     if error:
        return {"error": error}

     for product in products:
        if(product["id"]==product_id):
            product.update(data)
            return product
        return None
    
def delete_product(product_id):    
    for product in products:
        if(product["id"]==product_id):
            products.remove(product)
            break