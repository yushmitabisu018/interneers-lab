from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..services.product_category_service import ProductCategoryService

services = ProductCategoryService()


@csrf_exempt
def categories_api(req):
    if (req.method== "POST"):
       try:
          data= json.loads(req.body)
          category =services.create_category(data)
          return JsonResponse(category.to_dict(), status=201)
       
       except ValueError as e:
         return JsonResponse({"error": str(e)}, status=400)
       
       except Exception:
         return JsonResponse({"error": "Something went wrong"}, status=500)
       
    if (req.method== "GET"):
        categories =services.get_all_categories()
        data =[c.to_dict() for c in categories]
        return JsonResponse(data, safe=False)


@csrf_exempt
def categories_detail_api(req, category_id):
    if req.method=="GET":
       category = services.get_category(category_id)

       if not category:
         return JsonResponse({"error": "Category not found"}, status=404)
       return JsonResponse(category.to_dict())
    
    if req.method =="PUT":
        try:
         update_data= json.loads(req.body)
         category = services.update_category(category_id, update_data)

         if not category:
          return JsonResponse({"error": "Category not found"}, status=404)

         return JsonResponse(category.to_dict())
        
        except ValueError as e:
         return JsonResponse({"error": str(e)}, status=400)
        
        except Exception:
          return JsonResponse({"error": "Something went wrong"}, status=500)
    
    if (req.method== "DELETE"):
        value =services.delete_category(category_id)
        if not value:
            return JsonResponse({"error": "Category not found"}, status=404)

        return JsonResponse({"message": "Category deleted successfully"})
    

@csrf_exempt
def category_products_api(req, category_id):
    if req.method == "GET":
      try:
       products = services.get_products_by_category(category_id)
       data = [p.to_dict() for p in products]
       return JsonResponse(data, safe=False)
      
      except ValueError as e:
       return JsonResponse({"error": str(e)}, status=400)

      except Exception:
         return JsonResponse({"error": "Something went wrong"}, status=500)
 

@csrf_exempt
def category_product_detail_api(req, category_id, product_id): 
    #add
    if (req.method =="POST"):
     try: 
      product = services.add_product_to_category(category_id, product_id)
      return JsonResponse(product.to_dict())
     
     except ValueError as e:
      return JsonResponse({"error": str(e)}, status=400)
 
     except Exception:
       return JsonResponse({"error": "Something went wrong"}, status=500)
    
    #remove
    if req.method== "DELETE":
     try:
      product = services.remove_product_from_category(category_id, product_id)
      return JsonResponse(product.to_dict())
         
     except ValueError as e:
      return JsonResponse({"error": str(e)}, status=400)
     
     except Exception:
       return JsonResponse({"error": "Something went wrong"}, status=500)
   