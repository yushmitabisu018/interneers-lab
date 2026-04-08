from django.http import JsonResponse
from ..services.product_serivce import ProductService
import json
from django.views.decorators.csrf import csrf_exempt

def get_product_service():
  return ProductService()

@csrf_exempt
def products_api(req, service=None):
    if service is None:
        service= get_product_service()

    if req.method=="POST":
        data = json.loads(req.body)
        product = service.create_product(data)
        return JsonResponse(product.to_dict(), status=201)  
    
    if req.method=="GET":
        products = service.get_all()
        products_list = [p.to_dict() for p in products]
        return JsonResponse(products_list,safe=False)
     
@csrf_exempt
def products_detail_api(req, product_id, service=None):
    if service is None:
        service= get_product_service()

    if req.method=="GET":
        product = service.get_product(product_id)

        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)
        
        return JsonResponse(product.to_dict())

    if req.method=="PUT":
        data = json.loads(req.body)
        product = service.update_product(product_id,data)
    
        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)
    
        return JsonResponse(product.to_dict())
    
    if req.method=="DELETE":
        value = service.delete_product(product_id)

        if not value:
            return JsonResponse({"error":"Product not found"}, status=404)
        
        return JsonResponse({"message": "Product deleted successfully"})