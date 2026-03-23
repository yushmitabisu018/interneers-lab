from django.test import TestCase, Client
import json
from django.core.files.uploadedfile import SimpleUploadedFile


class Week4APITest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_category(self):
        response = self.client.post(
            "/week4/categories",
            data=json.dumps({
                "title": "Hair Care",
                "description": "Hair Products"
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("title", response.json())


    def test_get_categories(self):
        response = self.client.get("/week4/categories")
        self.assertEqual(response.status_code, 200)


    def test_create_product(self):
        response = self.client.post(
            "/week4/products",
            data=json.dumps({
                "name": "Shampoo",
                "brand": "Loreal",
                "price": 150
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Shampoo")

    def test_product_validation(self):
        response = self.client.post(
            "/week4/products",
            data=json.dumps({
                "name": "Oil",
                "price": 200
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_price(self):
        response = self.client.post(
            "/week4/products",
            data=json.dumps({
                "name": "Bad Product",
                "brand": "X",
                "price": -10
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)


    def test_add_product_to_category(self):
        #create cat first
        cat = self.client.post(
            "/week4/categories",
            data=json.dumps({"title": "Shampoo"}),
            content_type="application/json"
        ).json()

        # create product
        prod = self.client.post(
            "/week4/products",
            data=json.dumps({
                "name": "Hair Cream",
                "brand": "Loreal",
                "price": 400
            }),
            content_type="application/json"
        ).json()

        # adding product to cat
        response = self.client.post(
            f"/week4/categories/{cat['id']}/products/{prod['id']}"
        )

        self.assertEqual(response.status_code, 200)


    def test_filter_products(self):
        self.client.post(
            "/week4/products",
            data=json.dumps({
                "name": "Serum",
                "brand": "Dove",
                "price": 600
            }),
            content_type="application/json"
        )

        response = self.client.get("/week4/products?brand=Loreal")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 1)


    def test_bulk_upload(self):
        csv_content = b"name,brand,price\nConditioner,Pantene,500\nHairOil,Amla,200"

        file = SimpleUploadedFile(
            "test.csv",
            csv_content,
            content_type="text/csv"
        )

        response = self.client.post(
            "/week4/productsBulk/bulk-upload",
            {"file": file}
        )

        self.assertEqual(response.status_code, 200)