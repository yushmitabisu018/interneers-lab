from django.test import TestCase, Client
import json
# Create your tests here.

class ProductAPITest(TestCase):

    def setUp(self):
        self.client =Client()
        self.base_url = "/week3/products"
    def test_create_product(self):
        data = {
         "name": "Nothing Phone 1",
         "description": "SmartPhone",
         "category": "Electronics",
         "price": 50000,
         "brand": "Nothing",
         "quantity": 5
        }

        response = self.client.post(
            self.base_url,
            data = json.dumps(data),
            content_type="application/json"
        )   
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json()) #for checking if product contains id

    def test_get_products(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code,200)     
        
    def test_product_byId(self):
        data = {
            "name": "Mac",
            "description": "Laptop",
            "category": "Electronics",
            "price": 100000,
            "brand": "Apple",
            "quantity": 20
        }

        response = self.client.post(
            self.base_url,
            data=json.dumps(data),
            content_type="application/json"
        )

        product_id = response.json()["id"]

        # Get by id
        response = self.client.get(f"{self.base_url}/{product_id}")
        self.assertEqual(response.status_code, 200)

        # put
        update_data = {"price": 70000, "quantity": 10}
        response = self.client.put(
            f"{self.base_url}/{product_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        # delete
        response = self.client.delete(f"{self.base_url}/{product_id}")
        self.assertEqual(response.status_code, 200)