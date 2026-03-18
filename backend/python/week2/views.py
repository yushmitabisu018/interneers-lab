from django.shortcuts import render
from django.http import JsonResponse
import json
from .service import create_product, get_products, get_product, update_product, delete_product
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
#Api functions
@csrf_exempt
def products_view(req):

    if(req.method == "POST"):
        body = json.loads(req.body)
        product = create_product(body)
        
        if "error" in product:
            return JsonResponse(product, status=400)
        
        return JsonResponse(product, status=201)
    
    elif (req.method=="GET"):
        try:
         page = int(req.GET.get("page", 1))
         limit = int(req.GET.get("limit", 5))

         if page<1 or limit<1:
                raise ValueError

        except ValueError:
            return JsonResponse({"error": "Invalid pagination parameters"},status=400)
        
        products = get_products(page,limit)
        return JsonResponse(products, safe=False)
    
    return JsonResponse({"error": "Inavlid request method"})

@csrf_exempt
def product_detail_view(req, product_id):

    if(req.method=="GET"):
        product = get_product(product_id)

        if(product):
            return JsonResponse(product)
        
        return JsonResponse({"error": "Product not found"}, status=404)

    elif(req.method== "PUT"):
        body = json.loads(req.body)
        product = update_product(product_id, body)
        
        if product is None:
            return JsonResponse({"error": "Product not found"}, status=404)
        
        if "error" in product:
            return JsonResponse(product, status=400)
        
        return JsonResponse(product)

    elif(req.method=="DELETE"):
        delete_product(product_id)

        return JsonResponse({"message": "Product deleted successfully"}, status=200)
    
    return JsonResponse({"error": "Invalid request method"})