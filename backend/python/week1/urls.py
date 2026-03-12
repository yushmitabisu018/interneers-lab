from django.urls import path
from .views import hello, home


urlpatterns = [
    path('', home),
    path("hello/", hello),
]