# -*- coding: utf-8 -*-
"""
=============================================================================
UNIT TESTS - Price History Module
=============================================================================
Автор: Цвета Попова
Дата: 30 Октомври 2025
Цел: Unit тестове за price history функционалност
=============================================================================
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from backend.services.price_service import PriceHistoryService


class TestPriceHistoryService(unittest.TestCase):
    """Unit тестове за PriceHistoryService"""
    
    def setUp(self):
        """Setup преди всеки тест"""
        self.service = PriceHistoryService()
        self.test_asin = 'B08N5WRWNW'
    
    @patch('backend.services.price_service.database')
    def test_add_price_record(self, mock_db):
        """Тест: Добавяне на ценови запис"""
        mock_db.insert_price.return_value = True
        
        result = self.service.add_price_record(
            asin=self.test_asin,
            price=49.99,
            currency='USD'
        )
        
        self.assertTrue(result)
        mock_db.insert_price.assert_called_once()
    
    @patch('backend.services.price_service.database')
    def test_get_price_history(self, mock_db):
        """Тест: Извличане на ценова история"""
        mock_history = [
            {'price': 49.99, 'recorded_at': datetime.now()},
            {'price': 45.99, 'recorded_at': datetime.now() - timedelta(days=7)},
            {'price': 54.99, 'recorded_at': datetime.now() - timedelta(days=14)}
        ]
        mock_db.get_price_history.return_value = mock_history
        
        history = self.service.get_price_history(self.test_asin, days=30)
        
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['price'], 49.99)
    
    def test_calculate_price_change_percentage(self):
        """Тест: Изчисляване на процент промяна в цената"""
        old_price = 50.00
        new_price = 45.00
        
        change = self.service.calculate_price_change_percentage(old_price, new_price)
        
        self.assertEqual(change, -10.0)  # -10% намаление
    
    def test_calculate_price_statistics(self):
        """Тест: Изчисляване на статистики за цени"""
        price_history = [
            {'price': 49.99},
            {'price': 45.99},
            {'price': 54.99},
            {'price': 47.99}
        ]
        
        stats = self.service.calculate_statistics(price_history)
        
        self.assertIn('min_price', stats)
        self.assertIn('max_price', stats)
        self.assertIn('avg_price', stats)
        self.assertEqual(stats['min_price'], 45.99)
        self.assertEqual(stats['max_price'], 54.99)
    
    @patch('backend.services.price_service.database')
    def test_detect_price_drop(self, mock_db):
        """Тест: Детекция на спад в цената"""
        mock_db.get_latest_prices.return_value = [
            {'price': 45.00, 'recorded_at': datetime.now()},
            {'price': 60.00, 'recorded_at': datetime.now() - timedelta(days=1)}
        ]
        
        is_drop = self.service.detect_significant_price_drop(self.test_asin, threshold=20)
        
        self.assertTrue(is_drop)  # 25% спад е над 20% threshold


if __name__ == '__main__':
    unittest.main()
