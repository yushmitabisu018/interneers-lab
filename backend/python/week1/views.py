# Create your views here.

# handles api
from django.http import JsonResponse
from .service import greet

def home(request):
    return JsonResponse({"message": "API is running"})

def hello(request):
    name = request.GET.get("name", "Unknown")
    msg = greet(name)
    return JsonResponse({"message": msg})
