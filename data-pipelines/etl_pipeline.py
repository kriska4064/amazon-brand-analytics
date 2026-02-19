# -*- coding: utf-8 -*-
"""
=============================================================================
ETL PIPELINE - Extract, Transform, Load
=============================================================================
Автор: Диана Георгиева
Дата: 15 Юли 2025
Цел: ETL pipeline за обработка на Amazon данни
=============================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AmazonETLPipeline:
    """ETL Pipeline за обработка на Amazon данни"""
    
    def __init__(self):
        """Инициализация на ETL pipeline"""
        self.data = None
        self.cleaned_data = None
    
    def extract(self, source_path: str) -> pd.DataFrame:
        """
        EXTRACT: Извличане на данни от CSV файл
        
        Args:
            source_path: Път до CSV файла
            
        Returns:
            Pandas DataFrame с raw данни
        """
        logger.info(f"Извличане на данни от {source_path}")
        
        try:
            df = pd.read_csv(source_path, encoding='utf-8')
            logger.info(f"Успешно извлечени {len(df)} реда")
            self.data = df
            return df
        except Exception as e:
            logger.error(f"Грешка при извличане на данни: {e}")
            return pd.DataFrame()
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        TRANSFORM: Трансформация и почистване на данни
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Почистен и трансформиран DataFrame
        """
        logger.info("Започване на трансформация на данни")
        
        df_clean = df.copy()
        
        # 1. Премахване на дубликати
        initial_rows = len(df_clean)
        df_clean = df_clean.drop_duplicates(subset=['asin'], keep='first')
        logger.info(f"Премахнати {initial_rows - len(df_clean)} дубликати")
        
        # 2. Обработка на липсващи стойности
        df_clean['title'] = df_clean['title'].fillna('Unknown')
        df_clean['brand'] = df_clean['brand'].fillna('Generic')
        df_clean['category'] = df_clean['category'].fillna('Other')
        
        # 3. Почистване на цени
        if 'price' in df_clean.columns:
            df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')
            df_clean['price'] = df_clean['price'].fillna(df_clean['price'].median())
            df_clean['price'] = df_clean['price'].round(2)
        
        # 4. Валидация на рейтинги (0-5)
        if 'rating' in df_clean.columns:
            df_clean['rating'] = pd.to_numeric(df_clean['rating'], errors='coerce')
            df_clean['rating'] = df_clean['rating'].clip(0, 5)
            df_clean['rating'] = df_clean['rating'].fillna(0)
        
        # 5. Почистване на reviews_count
        if 'reviews_count' in df_clean.columns:
            df_clean['reviews_count'] = pd.to_numeric(df_clean['reviews_count'], errors='coerce')
            df_clean['reviews_count'] = df_clean['reviews_count'].fillna(0).astype(int)
        
        # 6. Нормализиране на ASIN формат
        if 'asin' in df_clean.columns:
            df_clean['asin'] = df_clean['asin'].str.upper().str.strip()
        
        # 7. Добавяне на изчислени колони
        df_clean['popularity_score'] = self._calculate_popularity_score(df_clean)
        df_clean['price_category'] = self._categorize_price(df_clean['price'])
        df_clean['rating_category'] = self._categorize_rating(df_clean['rating'])
        
        # 8. Добавяне на timestamps
        df_clean['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"Трансформация завършена: {len(df_clean)} валидни реда")
        self.cleaned_data = df_clean
        return df_clean
    
    def _calculate_popularity_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Изчисляване на popularity score базиран на rating и reviews
        
        Formula: (rating * 20) + log10(reviews_count + 1) * 10
        """
        if 'rating' in df.columns and 'reviews_count' in df.columns:
            score = (df['rating'] * 20) + (np.log10(df['reviews_count'] + 1) * 10)
            return score.round(2)
        return pd.Series([0] * len(df))
    
    def _categorize_price(self, prices: pd.Series) -> pd.Series:
        """Категоризиране на цени"""
        return pd.cut(
            prices,
            bins=[0, 20, 50, 100, 200, float('inf')],
            labels=['Budget', 'Economy', 'Mid-range', 'Premium', 'Luxury']
        )
    
    def _categorize_rating(self, ratings: pd.Series) -> pd.Series:
        """Категоризиране на рейтинги"""
        return pd.cut(
            ratings,
            bins=[0, 2, 3, 4, 4.5, 5],
            labels=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
        )
    
    def load(self, df: pd.DataFrame, output_path: str):
        """
        LOAD: Запазване на обработени данни
        
        Args:
            df: Обработен DataFrame
            output_path: Път за запазване
        """
        logger.info(f"Запазване на данни в {output_path}")
        
        try:
            df.to_csv(output_path, index=False, encoding='utf-8')
            logger.info(f"Данните успешно запазени ({len(df)} реда)")
        except Exception as e:
            logger.error(f"Грешка при запазване на данни: {e}")
    
    def run_pipeline(self, source_path: str, output_path: str):
        """
        Изпълнение на пълния ETL pipeline
        
        Args:
            source_path: Входен CSV файл
            output_path: Изходен CSV файл
        """
        logger.info("=== Стартиране на ETL Pipeline ===")
        
        # Extract
        raw_data = self.extract(source_path)
        if raw_data.empty:
            logger.error("Няма данни за обработка")
            return
        
        # Transform
        clean_data = self.transform(raw_data)
        
        # Load
        self.load(clean_data, output_path)
        
        logger.info("=== ETL Pipeline завършен успешно ===")
        
        # Статистики
        self.print_statistics(clean_data)
    
    def print_statistics(self, df: pd.DataFrame):
        """Принтиране на статистики"""
        print("\n" + "="*50)
        print("СТАТИСТИКИ НА ОБРАБОТЕНИТЕ ДАННИ")
        print("="*50)
        print(f"Общо продукти: {len(df)}")
        print(f"Уникални марки: {df['brand'].nunique()}")
        print(f"Категории: {df['category'].nunique()}")
        print(f"\nСредна цена: ${df['price'].mean():.2f}")
        print(f"Среден рейтинг: {df['rating'].mean():.2f}")
        print(f"Общо ревюта: {df['reviews_count'].sum():,}")
        print("="*50 + "\n")


def main():
    """Тестване на ETL pipeline"""
    
    pipeline = AmazonETLPipeline()
    
    # Изпълнение на pipeline
    pipeline.run_pipeline(
        source_path='amazon_products_raw.csv',
        output_path='amazon_products_clean.csv'
    )


if __name__ == '__main__':
    main()
