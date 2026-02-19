# -*- coding: utf-8 -*-
"""
=============================================================================
UNIT TESTS - Products Module
=============================================================================
Автор: Цвета Попова
Дата: 28 Октомври 2025
Цел: Unit тестове за products модул
=============================================================================
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Добавяне на parent directory към path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.models.product import Product
from backend.services.product_service import ProductService


class TestProductModel(unittest.TestCase):
    """Unit тестове за Product модел"""
    
    def setUp(self):
        """Setup преди всеки тест"""
        self.product_data = {
            'asin': 'B08N5WRWNW',
            'title': 'Amazon Echo Dot (4th Gen)',
            'brand': 'Amazon',
            'category': 'Electronics',
            'price': 49.99,
            'currency': 'USD',
            'rating': 4.7,
            'reviews_count': 15234
        }
    
    def test_product_creation(self):
        """Тест: Създаване на Product обект"""
        product = Product(**self.product_data)
        
        self.assertEqual(product.asin, 'B08N5WRWNW')
        self.assertEqual(product.title, 'Amazon Echo Dot (4th Gen)')
        self.assertEqual(product.brand, 'Amazon')
        self.assertEqual(product.price, 49.99)
        self.assertEqual(product.rating, 4.7)
    
    def test_product_validation_invalid_asin(self):
        """Тест: Валидация - невалиден ASIN"""
        invalid_data = self.product_data.copy()
        invalid_data['asin'] = 'INVALID'  # ASIN трябва да е 10 символа
        
        with self.assertRaises(ValueError):
            Product(**invalid_data)
    
    def test_product_validation_invalid_price(self):
        """Тест: Валидация - негативна цена"""
        invalid_data = self.product_data.copy()
        invalid_data['price'] = -10.00
        
        with self.assertRaises(ValueError):
            Product(**invalid_data)
    
    def test_product_validation_rating_range(self):
        """Тест: Валидация - рейтинг извън диапазон (0-5)"""
        invalid_data = self.product_data.copy()
        invalid_data['rating'] = 6.0
        
        with self.assertRaises(ValueError):
            Product(**invalid_data)
    
    def test_product_to_dict(self):
        """Тест: Конвертиране на Product към dict"""
        product = Product(**self.product_data)
        product_dict = product.to_dict()
        
        self.assertIsInstance(product_dict, dict)
        self.assertEqual(product_dict['asin'], 'B08N5WRWNW')
        self.assertEqual(product_dict['brand'], 'Amazon')


class TestProductService(unittest.TestCase):
    """Unit тестове за ProductService"""
    
    def setUp(self):
        """Setup преди всеки тест"""
        self.service = ProductService()
    
    @patch('backend.services.product_service.database')
    def test_get_product_by_asin(self, mock_db):
        """Тест: Извличане на продукт по ASIN"""
        mock_db.get_product.return_value = {
            'asin': 'B08N5WRWNW',
            'title': 'Amazon Echo Dot (4th Gen)',
            'brand': 'Amazon',
            'price': 49.99
        }
        
        product = self.service.get_product_by_asin('B08N5WRWNW')
        
        self.assertIsNotNone(product)
        self.assertEqual(product['asin'], 'B08N5WRWNW')
        mock_db.get_product.assert_called_once_with('B08N5WRWNW')
    
    @patch('backend.services.product_service.database')
    def test_search_products_by_brand(self, mock_db):
        """Тест: Търсене на продукти по марка"""
        mock_db.search_by_brand.return_value = [
            {'asin': 'B001', 'brand': 'Amazon', 'title': 'Product 1'},
            {'asin': 'B002', 'brand': 'Amazon', 'title': 'Product 2'}
        ]
        
        products = self.service.search_by_brand('Amazon')
        
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]['brand'], 'Amazon')
        mock_db.search_by_brand.assert_called_once_with('Amazon')
    
    @patch('backend.services.product_service.database')
    def test_calculate_average_rating(self, mock_db):
        """Тест: Изчисляване на среден рейтинг"""
        mock_db.get_products_by_brand.return_value = [
            {'rating': 4.5},
            {'rating': 4.7},
            {'rating': 4.3}
        ]
        
        avg_rating = self.service.calculate_average_rating('Amazon')
        
        self.assertAlmostEqual(avg_rating, 4.5, places=1)


if __name__ == '__main__':
    unittest.main()
