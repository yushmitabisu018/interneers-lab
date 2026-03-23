from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..services.product_service import ProductService

services = ProductService()

@csrf_exempt
def products_api(req):
    if req.method == "POST":
       try: 
        data = json.loads(req.body)
        product = services.create_product(data)

        return JsonResponse(product.to_dict(), status=201)
       
       except ValueError as e:
         return JsonResponse({"error": str(e)}, status=400)
       
       except Exception:
         return JsonResponse({"error": "Something went wrong"}, status=500)
       
    if req.method == "GET":
        try: 
            filters = {
              "categories":req.GET.getlist("categories"),
              "price_min": req.GET.get("price_min"),
               "price_max":req.GET.get("price_max"),
               "brand": req.GET.get("brand"),
                "sort": req.GET.get("sort"),
                "page": req.GET.get("page", 1),
                "limit": req.GET.get("limit", 10),
            }


            if filters["price_min"]:
                filters["price_min"] = float(filters["price_min"])

            if filters["price_max"]:
                filters["price_max"] = float(filters["price_max"])

            products = services.get_products(filters)
            products_list = [p.to_dict() for p in products]

            return JsonResponse(products_list, safe=False)
        
        except ValueError as e:
          return JsonResponse({"error": str(e)}, status=400)

        except Exception:
            return JsonResponse({"error": "Something went wrong"}, status=500)
        
@csrf_exempt
def product_detail_api(req, product_id):
    if req.method == "GET":
        product = services.get_product(product_id)

        if not product:
            return JsonResponse({"error": "Product not found"}, status=404)
        return JsonResponse(product.to_dict())

    if req.method == "PUT":
        try:   
            data = json.loads(req.body)
            product = services.update_product(product_id, data)

            if not product:
              return JsonResponse({"error": "Product not found"}, status=404)

            return JsonResponse(product.to_dict())
        
        except ValueError as e:
          return JsonResponse({"error": str(e)}, status=400)
        
        except Exception:
            return JsonResponse({"error": "Something went wrong"}, status=500)
   
    if req.method =="DELETE":
        value = services.delete_product(product_id)

        if not value:
            return JsonResponse({"error": "Product not found"}, status=404)

        return JsonResponse({"message": "Product deleted successfully"})
    
@csrf_exempt
def bulk_upload_products(req):
    if req.method == "POST":
       try: 
        file = req.FILES.get("file")
        if not file:
         return JsonResponse({"error": "CSV file required"}, status=400)

        products = services.bulk_create_products(file)
        data = [p.to_dict() for p in products]
        return JsonResponse(data, safe=False)
      
       except ValueError as e:
         return JsonResponse({"error": str(e)}, status=400)

       except Exception:
         return JsonResponse({"error": "Something went wrong"}, status=500)
      