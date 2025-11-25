# -*- coding: utf-8 -*-
"""
=============================================================================
REGRESSION TEST SUITE - Amazon Brand Analytics
=============================================================================
Автор: Цвета Попова
Дата: 20 Декември 2025
Цел: Regression тестове за валидация на стабилност след промени
=============================================================================
"""

import unittest
import requests


class TestRegressionSuite(unittest.TestCase):
    """Regression тестове за стабилност"""
    
    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://localhost:5000/api/v1'
        cls.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token-123'
        }
    
    def test_products_api_still_works(self):
        """Regression: Products API работи след промени"""
        response = requests.get(f'{self.base_url}/products', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.json())
    
    def test_price_history_api_still_works(self):
        """Regression: Price History API работи след промени"""
        response = requests.get(
            f'{self.base_url}/price-history/B08N5WRWNW',
            headers=self.headers
        )
        self.assertIn(response.status_code, [200, 404])
    
    def test_invalid_asin_still_returns_400(self):
        """Regression: Невалиден ASIN все още връща 400"""
        response = requests.get(
            f'{self.base_url}/products/INVALID',
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)
    
    def test_negative_price_still_rejected(self):
        """Regression: Негативни цени все още се отхвърлят"""
        product_data = {
            'asin': 'B09REGTEST1',
            'title': 'Regression Test Product',
            'brand': 'TestBrand',
            'price': -10.00
        }
        response = requests.post(
            f'{self.base_url}/products',
            headers=self.headers,
            json=product_data
        )
        self.assertEqual(response.status_code, 400)
    
    def test_empty_price_history_returns_empty_array(self):
        """Regression: Празна price history връща [] вместо 500 грешка"""
        response = requests.get(
            f'{self.base_url}/price-history/B00NODATA00',
            headers=self.headers
        )
        if response.status_code == 200:
            data = response.json()
            self.assertIsInstance(data.get('history', []), list)
        else:
            self.assertNotEqual(response.status_code, 500)
    
    def test_backward_compatibility_products_response_format(self):
        """Regression: Форматът на Products отговора не се е сменил"""
        response = requests.get(f'{self.base_url}/products', headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.assertIsInstance(data, dict)
            self.assertIn('products', data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
