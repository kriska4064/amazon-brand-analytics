# -*- coding: utf-8 -*-
"""
=============================================================================
COMPETITOR ANALYSIS - Анализ на конкуренти
=============================================================================
Автор: Диана Георгиева
Дата: 25 Октомври 2025
Цел: Анализ на конкурентни марки и пазарен дял
=============================================================================
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')


class CompetitorAnalyzer:
    """Клас за анализ на конкуренти"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Инициализация на анализатор
        
        Args:
            data: DataFrame с продуктови данни
        """
        self.data = data
        self.competitor_stats = None
    
    def analyze_by_brand(self) -> pd.DataFrame:
        """
        Анализ по марки
        
        Returns:
            DataFrame със статистики по марки
        """
        brand_stats = self.data.groupby('brand').agg({
            'asin': 'count',
            'price': ['mean', 'median', 'std'],
            'rating': 'mean',
            'reviews_count': 'sum'
        }).round(2)
        
        brand_stats.columns = ['total_products', 'avg_price', 'median_price', 
                                'price_std', 'avg_rating', 'total_reviews']
        
        # Пазарен дял (по брой продукти)
        brand_stats['market_share_pct'] = (
            brand_stats['total_products'] / brand_stats['total_products'].sum() * 100
        ).round(2)
        
        # Сортиране по пазарен дял
        brand_stats = brand_stats.sort_values('market_share_pct', ascending=False)
        
        self.competitor_stats = brand_stats
        return brand_stats
    
    def get_top_competitors(self, n: int = 10) -> pd.DataFrame:
        """
        Топ N конкуренти по пазарен дял
        
        Args:
            n: Брой конкуренти
            
        Returns:
            DataFrame с топ конкуренти
        """
        if self.competitor_stats is None:
            self.analyze_by_brand()
        
        return self.competitor_stats.head(n)
    
    def price_positioning_analysis(self) -> Dict:
        """
        Анализ на ценово позициониране
        
        Returns:
            Речник с анализ
        """
        if self.competitor_stats is None:
            self.analyze_by_brand()
        
        analysis = {
            'premium_brands': self.competitor_stats[
                self.competitor_stats['avg_price'] > self.competitor_stats['avg_price'].quantile(0.75)
            ].index.tolist(),
            
            'mid_range_brands': self.competitor_stats[
                (self.competitor_stats['avg_price'] >= self.competitor_stats['avg_price'].quantile(0.25)) &
                (self.competitor_stats['avg_price'] <= self.competitor_stats['avg_price'].quantile(0.75))
            ].index.tolist(),
            
            'budget_brands': self.competitor_stats[
                self.competitor_stats['avg_price'] < self.competitor_stats['avg_price'].quantile(0.25)
            ].index.tolist()
        }
        
        return analysis
    
    def quality_vs_price_analysis(self) -> pd.DataFrame:
        """
        Анализ качество (rating) vs цена
        
        Returns:
            DataFrame с класификация
        """
        if self.competitor_stats is None:
            self.analyze_by_brand()
        
        df = self.competitor_stats.copy()
        
        # Класификация
        median_price = df['avg_price'].median()
        median_rating = df['avg_rating'].median()
        
        def classify(row):
            if row['avg_price'] >= median_price and row['avg_rating'] >= median_rating:
                return 'Premium Quality'
            elif row['avg_price'] < median_price and row['avg_rating'] >= median_rating:
                return 'Value for Money'
            elif row['avg_price'] >= median_price and row['avg_rating'] < median_rating:
                return 'Overpriced'
            else:
                return 'Budget'
        
        df['positioning'] = df.apply(classify, axis=1)
        
        return df[['avg_price', 'avg_rating', 'positioning', 'market_share_pct']]
    
    def competitive_advantage_score(self) -> pd.DataFrame:
        """
        Изчисляване на конкурентно предимство
        
        Returns:
            DataFrame с competitive advantage score
        """
        if self.competitor_stats is None:
            self.analyze_by_brand()
        
        df = self.competitor_stats.copy()
        
        # Нормализиране на метриките (0-100)
        df['rating_score'] = (df['avg_rating'] / 5) * 100
        df['market_share_score'] = (df['market_share_pct'] / df['market_share_pct'].max()) * 100
        df['review_volume_score'] = (df['total_reviews'] / df['total_reviews'].max()) * 100
        
        # Инвертиране на цената (по-ниска цена = по-добър скор)
        df['price_competitiveness'] = (1 - (df['avg_price'] / df['avg_price'].max())) * 100
        
        # Общ скор (weighted average)
        df['competitive_advantage_score'] = (
            df['rating_score'] * 0.3 +
            df['market_share_score'] * 0.25 +
            df['review_volume_score'] * 0.25 +
            df['price_competitiveness'] * 0.2
        ).round(2)
        
        return df[['competitive_advantage_score', 'rating_score', 'market_share_score', 
                   'review_volume_score', 'price_competitiveness']].sort_values(
            'competitive_advantage_score', ascending=False
        )
    
    def generate_competitor_report(self, output_path: str = 'competitor_analysis_report.txt'):
        """
        Генериране на текстов отчет
        
        Args:
            output_path: Път за запазване на отчета
        """
        if self.competitor_stats is None:
            self.analyze_by_brand()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("ОТЧЕТ ЗА КОНКУРЕНТЕН АНАЛИЗ\n")
            f.write("="*70 + "\n\n")
            
            # Топ 10 конкуренти
            f.write("ТОП 10 КОНКУРЕНТИ ПО ПАЗАРЕН ДЯЛ:\n")
            f.write("-"*70 + "\n")
            top10 = self.get_top_competitors(10)
            for idx, (brand, row) in enumerate(top10.iterrows(), 1):
                f.write(f"{idx}. {brand}\n")
                f.write(f"   Пазарен дял: {row['market_share_pct']}%\n")
                f.write(f"   Средна цена: ${row['avg_price']:.2f}\n")
                f.write(f"   Среден рейтинг: {row['avg_rating']:.2f}\n")
                f.write(f"   Общо ревюта: {row['total_reviews']:,}\n\n")
            
            # Ценово позициониране
            f.write("\n" + "="*70 + "\n")
            f.write("ЦЕНОВО ПОЗИЦИОНИРАНЕ:\n")
            f.write("-"*70 + "\n")
            positioning = self.price_positioning_analysis()
            f.write(f"Premium марки: {', '.join(positioning['premium_brands'][:5])}\n")
            f.write(f"Mid-range марки: {', '.join(positioning['mid_range_brands'][:5])}\n")
            f.write(f"Budget марки: {', '.join(positioning['budget_brands'][:5])}\n")
            
            # Competitive advantage
            f.write("\n" + "="*70 + "\n")
            f.write("ТОП 5 ПО КОНКУРЕНТНО ПРЕДИМСТВО:\n")
            f.write("-"*70 + "\n")
            advantage = self.competitive_advantage_score()
            for idx, (brand, row) in enumerate(advantage.head(5).iterrows(), 1):
                f.write(f"{idx}. {brand} - Скор: {row['competitive_advantage_score']:.2f}\n")
        
        print(f"✓ Отчетът е запазен в {output_path}")


def main():
    """Тестване"""
    # Зареждане на данни
    data = pd.read_csv('amazon_products_clean.csv')
    
    # Анализ
    analyzer = CompetitorAnalyzer(data)
    
    # Статистики по марки
    brand_stats = analyzer.analyze_by_brand()
    print("\nТоп 5 конкуренти:")
    print(analyzer.get_top_competitors(5))
    
    # Генериране на отчет
    analyzer.generate_competitor_report()


if __name__ == '__main__':
    main()
