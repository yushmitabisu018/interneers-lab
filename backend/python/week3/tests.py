from django.test import TestCase, Client
import json
from week3.models import Product
# Create your tests here.

class ProductAPITest(TestCase):
    def setUp(self):
        self.client =Client()
        self.base_url = "/week3/products"

    def tearDown(self):
        Product.objects.delete()   

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

    def test_get_all_products(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code,200)     
        
    def test_get_product(self):
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

        response = self.client.get(f"{self.base_url}/{product_id}")
        self.assertEqual(response.status_code, 200)

    def test_update_product(self):
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

        #update
        update_data = {"price": 70000, "quantity": 10}
        response = self.client.put(
            f"{self.base_url}/{product_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
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
        #delete
        response = self.client.delete(f"{self.base_url}/{product_id}")
        self.assertEqual(response.status_code, 200)
    

    def test_get_non_existent_product_id(self):
        non_existent_id = 9999
        response = self.client.get(f"{self.base_url}/{non_existent_id}")
        self.assertEqual(response.status_code, 404)

    def test_update_non_existent_product_id(self):
        non_existent_id = 9999
        update_data = {"price": 1000}
        response = self.client.put(
            f"{self.base_url}/{non_existent_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_non_existent_product_id(self):
        non_existent_id = 9999
        response = self.client.delete(f"{self.base_url}/{non_existent_id}")
        self.assertEqual(response.status_code, 404)
    
    def test_post_invalid_json(self):
        invalid_json = "{name: invalid json}"
        response = self.client.post(
            self.base_url,
            data=invalid_json,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


    def test_post_missing_name(self):
        data = {
            "description": "SmartPhone",
            "category": "Electronics",
            "price": 50000,
            "brand": "Test",
            "quantity": 5
        }

        response = self.client.post(
            self.base_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_missing_price(self):
        data = {
            "name": "Test Product",
            "description": "SmartPhone",
            "category": "Electronics",
            "brand": "Test",
            "quantity": 5
        }

        response = self.client.post(
            self.base_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


    def test_get_malformed_product_id(self):
        malformed_id = "abc"
        response = self.client.get(f"{self.base_url}/{malformed_id}")
        self.assertEqual(response.status_code, 400)

    def test_update_malformed_product_id(self):
        malformed_id = "abc"
        update_data = {"price": 2000}
        response = self.client.put(
            f"{self.base_url}/{malformed_id}",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_malformed_product_id(self):
        malformed_id = "abc"
        response = self.client.delete(f"{self.base_url}/{malformed_id}")
        self.assertEqual(response.status_code, 400)    