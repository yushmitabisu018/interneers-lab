from django.http import JsonResponse
from ..services.product_serivce import ProductService
import json
from django.views.decorators.csrf import csrf_exempt

services = ProductService()

@csrf_exempt
def products_api(req):
    if(req.method=="POST"):
        data = json.loads(req.body)
        product = services.create_product(data)
        return JsonResponse(product.to_dict(), status=201)  
    
    if(req.method=="GET"):
        products = services.get_all()
        products_list = [p.to_dict() for p in products]
        return JsonResponse(products_list,safe=False)
     
@csrf_exempt
def products_detail_api(req, product_id):
    # print("rec:", product_id)
    if(req.method=="GET"):
        product = services.get_product(product_id)

        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)
        
        return JsonResponse(product.to_dict())

    if(req.method=="PUT"):
        data = json.loads(req.body)
        product = services.update_product(product_id,data)
    
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)
    
        return JsonResponse(product.to_dict())
    
    if(req.method=="DELETE"):
        value = services.delete_product(product_id)

        if not value:
            return JsonResponse({"error":"Product not found"}, status=404)
        
        return JsonResponse({"message": "Product deleted successfully"})