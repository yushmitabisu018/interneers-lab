from django.test import TestCase, Client
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, ProductCategory


class Week4APITest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        Product.objects.delete()
        ProductCategory.objects.delete()

    def test_create_category(self):
        response = self.client.post(
            "/week4/categories/",
            data=json.dumps({
                "title": "Hair Care",
                "description": "Hair Products"
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn("title", response.json())


    def test_get_categories(self):
        response = self.client.get("/week4/categories/")
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
            f"/week4/categories/{cat['id']}/products/{prod['id']}/"
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

        response = self.client.get("/week4/products?brand=Dove")

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
            "/week4/products/bulk-upload/",
            {"file": file}
        )

        self.assertEqual(response.status_code, 200)


    def test_update_product(self):
        response = self.client.post(
            "/week4/products/",
            data=json.dumps({
                "name": "Shampoo",
                "brand": "Loreal",
                "price": 150
            }),
            content_type="application/json"
        )
        product_id = response.json()["id"]

        #update
        update_data = {"price": 200, "quantity": 10}
        response = self.client.put(
            f"/week4/products/{product_id}/",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)


    def test_delete_product(self):
        response = self.client.post(
            "/week4/products/",
            data=json.dumps({
                "name": "Shampoo",
                "brand": "Loreal",
                "price": 150
            }),
            content_type="application/json"
        )
        product_id = response.json()["id"]

        #delete
        response = self.client.delete(f"/week4/products/{product_id}/")
        self.assertEqual(response.status_code, 200)


    def test_update_category(self):
        response = self.client.post(
            "/week4/categories/",
            data=json.dumps({
                "title": "Hair Care",
                "description": "Hair Products"
            }),
            content_type="application/json"
        )
        category_id = response.json()["id"]

        #update category
        update_data = {"description": "New hair products"}
        response = self.client.put(
            f"/week4/categories/{category_id}/",
            data=json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)


    def test_delete_category(self):
        response = self.client.post(
            "/week4/categories/",
            data=json.dumps({
                "title": "Hair Care",
                "description": "Hair Products"
            }),
            content_type="application/json"
        )
        category_id = response.json()["id"]

        #delete category
        response = self.client.delete(f"/week4/categories/{category_id}/")
        self.assertEqual(response.status_code, 200)


    def test_remove_product_from_category(self):
        cat = self.client.post(
            "/week4/categories/",
            data=json.dumps({"title": "Shampoo"}),
            content_type="application/json"
        ).json()

        prod = self.client.post(
            "/week4/products/",
            data=json.dumps({
                "name": "Hair Cream",
                "brand": "Loreal",
                "price": 400
            }),
            content_type="application/json"
        ).json()

        #add product to category
        self.client.post(f"/week4/categories/{cat['id']}/products/{prod['id']}/")

        #remove product from category
        response = self.client.delete(f"/week4/categories/{cat['id']}/products/{prod['id']}/")
        self.assertEqual(response.status_code, 200)


    def test_get_invalid_product_id(self):
        response = self.client.get("/week4/products/invalid_id/")
        self.assertEqual(response.status_code, 404)

    def test_update_invalid_product_id(self):
        response = self.client.put(
            "/week4/products/invalid_id/",
            data=json.dumps({"price": 100}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_invalid_product_id(self):
        response = self.client.delete("/week4/products/invalid_id/")
        self.assertEqual(response.status_code, 404)


    def test_get_invalid_category_id(self):
        response = self.client.get("/week4/categories/invalid_id/")
        self.assertEqual(response.status_code, 404)

    def test_update_invalid_category_id(self):
        response = self.client.put(
            "/week4/categories/invalid_id/",
            data=json.dumps({"description": "test"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_invalid_category_id(self):
        response = self.client.delete("/week4/categories/invalid_id/")
        self.assertEqual(response.status_code, 404)


    def test_duplicate_category_title(self):
        #create category
        self.client.post(
            "/week4/categories/",
            data=json.dumps({
                "title": "Electronics",
                "description": "Electronic products"
            }),
            content_type="application/json"
        )

        #duplicate
        response = self.client.post(
            "/week4/categories/",
            data=json.dumps({
                "title": "Electronics",
                "description": "Products"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


    def test_pagination(self):
        #create multiple products
        for i in range(15):
            self.client.post(
                "/week4/products/",
                data=json.dumps({
                    "name": f"Product {i}",
                    "brand": "TestBrand",
                    "price": 100 + i
                }),
                content_type="application/json"
            )

        response = self.client.get("/week4/products?page=2&limit=5/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)