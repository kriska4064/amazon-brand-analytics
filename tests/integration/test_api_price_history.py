# -*- coding: utf-8 -*-
"""
=============================================================================
INTEGRATION TESTS - Price History API
=============================================================================
Автор: Цвета Попова
Дата: 18 Ноември 2025
Цел: Integration тестове за Price History API endpoints
=============================================================================
"""

import unittest
import requests
from datetime import datetime, timedelta


class TestPriceHistoryAPI(unittest.TestCase):
    """Integration тестове за Price History API"""
    
    @classmethod
    def setUpClass(cls):
        """Setup преди всички тестове"""
        cls.base_url = 'http://localhost:5000/api/v1'
        cls.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token-123'
        }
        cls.test_asin = 'B08N5WRWNW'
    
    def test_01_add_price_record(self):
        """Тест: POST /price-history - Добавяне на ценови запис"""
        price_data = {
            'asin': self.test_asin,
            'price': 49.99,
            'currency': 'USD'
        }
        
        response = requests.post(
            f'{self.base_url}/price-history',
            headers=self.headers,
            json=price_data
        )
        
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn('price_history_id', data)
        print(f"✓ Добавен ценови запис: {data['price_history_id']}")
    
    def test_02_get_price_history(self):
        """Тест: GET /price-history/{asin} - Извличане на ценова история"""
        response = requests.get(
            f'{self.base_url}/price-history/{self.test_asin}',
            headers=self.headers,
            params={'days': 30}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('history', data)
        self.assertIsInstance(data['history'], list)
        print(f"✓ Извлечени {len(data['history'])} ценови записа")
    
    def test_03_get_price_statistics(self):
        """Тест: GET /price-history/{asin}/stats - Статистики за цени"""
        response = requests.get(
            f'{self.base_url}/price-history/{self.test_asin}/stats',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn('min_price', data)
        self.assertIn('max_price', data)
        self.assertIn('avg_price', data)
        self.assertIn('current_price', data)
        
        print(f"✓ Статистики: Min={data['min_price']}, Max={data['max_price']}, Avg={data['avg_price']}")
    
    def test_04_detect_price_drops(self):
        """Тест: GET /price-history/drops - Детекция на спадове в цените"""
        response = requests.get(
            f'{self.base_url}/price-history/drops',
            headers=self.headers,
            params={'threshold': 20}  # 20% спад
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('price_drops', data)
        
        for drop in data['price_drops']:
            self.assertIn('asin', drop)
            self.assertIn('old_price', drop)
            self.assertIn('new_price', drop)
            self.assertIn('percentage_change', drop)
        
        print(f"✓ Открити {len(data['price_drops'])} значителни спада в цените")


if __name__ == '__main__':
    unittest.main(verbosity=2)
