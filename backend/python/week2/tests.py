from django.test import TestCase, Client
import json

# Create your tests here.
class ProductAPITest(TestCase):

    def setUp(self):
        self.client =Client()

    def test_create_product(self):
        data = {
         "name": "Laptop",
         "description": "Gaming laptop",
         "category": "Electronics",
         "price": 80000,
         "brand": "Asus",
         "quantity": 5
        }

        response = self.client.post(
            "/week2/products",
            data = json.dumps(data),
            content_type="application/json"
        )   
        self.assertEqual(response.status_code, 201)
        
    def test_get_product(self):
        
        response = self.client.get("/week2/products")
        self.assertEqual(response.status_code,200)     

    def test_pagination(self):

        response = self.client.get("/week2/products?page=1&limit=2")
        self.assertEqual(response.status_code, 200)

    def test_invalid_pagination(self):

        response = self.client.get("/week2/products?page=-1")
        self.assertEqual(response.status_code, 400)    