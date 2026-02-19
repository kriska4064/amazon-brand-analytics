# -*- coding: utf-8 -*-
"""
=============================================================================
INTEGRATION TESTS - Products API
=============================================================================
Автор: Цвета Попова
Дата: 15 Ноември 2025
Цел: Integration тестове за Products API endpoints
=============================================================================
"""

import unittest
import requests
import json
from datetime import datetime


class TestProductsAPI(unittest.TestCase):
    """Integration тестове за Products API"""
    
    @classmethod
    def setUpClass(cls):
        """Setup преди всички тестове"""
        cls.base_url = 'http://localhost:5000/api/v1'
        cls.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token-123'
        }
    
    def test_01_get_all_products(self):
        """Тест: GET /products - Извличане на всички продукти"""
        response = requests.get(
            f'{self.base_url}/products',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('products', data)
        self.assertIsInstance(data['products'], list)
        print(f"✓ Извлечени {len(data['products'])} продукта")
    
    def test_02_get_product_by_asin(self):
        """Тест: GET /products/{asin} - Извличане на конкретен продукт"""
        test_asin = 'B08N5WRWNW'
        response = requests.get(
            f'{self.base_url}/products/{test_asin}',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['asin'], test_asin)
        self.assertIn('title', data)
        self.assertIn('brand', data)
        print(f"✓ Продукт {test_asin}: {data['title']}")
    
    def test_03_create_product(self):
        """Тест: POST /products - Създаване на нов продукт"""
        new_product = {
            'asin': 'B09TEST123',
            'title': 'Test Product',
            'brand': 'TestBrand',
            'category': 'Electronics',
            'price': 29.99,
            'currency': 'USD',
            'rating': 4.5,
            'reviews_count': 100
        }
        
        response = requests.post(
            f'{self.base_url}/products',
            headers=self.headers,
            json=new_product
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['asin'], 'B09TEST123')
        print(f"✓ Създаден продукт: {data['asin']}")
    
    def test_04_update_product(self):
        """Тест: PUT /products/{asin} - Актуализация на продукт"""
        test_asin = 'B09TEST123'
        updated_data = {
            'price': 24.99,
            'rating': 4.7
        }
        
        response = requests.put(
            f'{self.base_url}/products/{test_asin}',
            headers=self.headers,
            json=updated_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['price'], 24.99)
        print(f"✓ Актуализиран продукт {test_asin}: нова цена {data['price']}")
    
    def test_05_search_products_by_brand(self):
        """Тест: GET /products/search?brand=X - Търсене по марка"""
        response = requests.get(
            f'{self.base_url}/products/search',
            headers=self.headers,
            params={'brand': 'Amazon'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data['results'], list)
        
        for product in data['results']:
            self.assertEqual(product['brand'], 'Amazon')
        
        print(f"✓ Намерени {len(data['results'])} продукта от марка Amazon")
    
    def test_06_filter_products_by_price_range(self):
        """Тест: GET /products/search?min_price=X&max_price=Y"""
        response = requests.get(
            f'{self.base_url}/products/search',
            headers=self.headers,
            params={'min_price': 20, 'max_price': 50}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        for product in data['results']:
            self.assertGreaterEqual(product['price'], 20)
            self.assertLessEqual(product['price'], 50)
        
        print(f"✓ Филтрирани {len(data['results'])} продукта в ценови диапазон 20-50")
    
    def test_07_delete_product(self):
        """Тест: DELETE /products/{asin} - Изтриване на продукт"""
        test_asin = 'B09TEST123'
        response = requests.delete(
            f'{self.base_url}/products/{test_asin}',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 204)
        print(f"✓ Изтрит продукт {test_asin}")
    
    def test_08_invalid_asin_format(self):
        """Тест: Невалиден ASIN формат"""
        response = requests.get(
            f'{self.base_url}/products/INVALID',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)
        print(f"✓ Валидация на невалиден ASIN: {data['error']}")


if __name__ == '__main__':
    # Изпълнение на тестовете в ред
    unittest.main(verbosity=2)
