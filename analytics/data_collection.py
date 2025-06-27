# -*- coding: utf-8 -*-
"""
=============================================================================
DATA COLLECTION - Amazon Products Data
=============================================================================
Автор: Диана Георгиева
Дата: 25 Юни 2025
Цел: Събиране и първична обработка на данни от Amazon API
=============================================================================
"""

import requests
import pandas as pd
from datetime import datetime
import logging
import json
from typing import List, Dict, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AmazonDataCollector:
    """Клас за събиране на данни от Amazon API"""
    
    def __init__(self, api_key: str, base_url: str):
        """
        Инициализация на data collector
        
        Args:
            api_key: API ключ за Amazon API
            base_url: Базов URL на API endpoint-а
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def collect_products(self, category: str, limit: int = 100) -> List[Dict]:
        """
        Събиране на продукти по категория
        
        Args:
            category: Категория на продуктите
            limit: Максимален брой продукти за извличане
            
        Returns:
            Списък с продуктови данни
        """
        logger.info(f"Започване на събиране на данни за категория: {category}")
        
        products = []
        offset = 0
        batch_size = 50
        
        while len(products) < limit:
            try:
                response = self.session.get(
                    f'{self.base_url}/products',
                    params={
                        'category': category,
                        'limit': batch_size,
                        'offset': offset
                    }
                )
                response.raise_for_status()
                
                data = response.json()
                batch_products = data.get('products', [])
                
                if not batch_products:
                    break
                
                products.extend(batch_products)
                offset += batch_size
                
                logger.info(f"Събрани {len(products)} продукта досега...")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Грешка при извличане на данни: {e}")
                break
        
        logger.info(f"Общо събрани продукти: {len(products)}")
        return products[:limit]
    
    def collect_price_history(self, asin: str, days: int = 30) -> List[Dict]:
        """
        Събиране на ценова история за продукт
        
        Args:
            asin: Amazon ASIN на продукта
            days: Брой дни назад за извличане
            
        Returns:
            Списък с ценови записи
        """
        logger.info(f"Събиране на ценова история за ASIN: {asin}")
        
        try:
            response = self.session.get(
                f'{self.base_url}/price-history/{asin}',
                params={'days': days}
            )
            response.raise_for_status()
            
            data = response.json()
            price_history = data.get('history', [])
            
            logger.info(f"Извлечени {len(price_history)} ценови записа")
            return price_history
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Грешка при извличане на ценова история: {e}")
            return []
    
    def collect_competitor_data(self, brand: str) -> Dict:
        """
        Събиране на данни за конкуренти по марка
        
        Args:
            brand: Име на марката
            
        Returns:
            Речник с конкурентни данни
        """
        logger.info(f"Събиране на конкурентни данни за марка: {brand}")
        
        try:
            response = self.session.get(
                f'{self.base_url}/competitors',
                params={'brand': brand}
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Конкурентни данни успешно събрани")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Грешка при извличане на конкурентни данни: {e}")
            return {}
    
    def save_to_dataframe(self, data: List[Dict]) -> pd.DataFrame:
        """
        Конвертиране на данни към Pandas DataFrame
        
        Args:
            data: Списък с речници
            
        Returns:
            Pandas DataFrame
        """
        df = pd.DataFrame(data)
        
        # Почистване на данни
        if 'price' in df.columns:
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
        
        if 'rating' in df.columns:
            df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
        
        if 'reviews_count' in df.columns:
            df['reviews_count'] = pd.to_numeric(df['reviews_count'], errors='coerce')
        
        logger.info(f"Създаден DataFrame с {len(df)} реда и {len(df.columns)} колони")
        return df
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """
        Запазване на данни в CSV файл
        
        Args:
            data: Списък с речници
            filename: Име на изходния файл
        """
        df = self.save_to_dataframe(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        logger.info(f"Данните са запазени в {filename}")


def main():
    """Основна функция за тестване"""
    
    # Инициализация
    collector = AmazonDataCollector(
        api_key='test-api-key-123',
        base_url='http://localhost:5000/api/v1'
    )
    
    # Събиране на продукти
    products = collector.collect_products(category='Electronics', limit=100)
    
    # Запазване в CSV
    collector.save_to_csv(products, 'amazon_products_electronics.csv')
    
    print(f"✓ Успешно събрани {len(products)} продукта")


if __name__ == '__main__':
    main()
