# -*- coding: utf-8 -*-
"""
=============================================================================
SALES DASHBOARD - Дашборд за продажби и анализи
=============================================================================
Автор: Диана Георгиева
Дата: 20 Август 2025
Цел: Интерактивен dashboard за визуализация на продажби
=============================================================================
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta


class SalesDashboard:
    """Клас за генериране на sales dashboard"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Инициализация на dashboard
        
        Args:
            data: DataFrame с продуктови данни
        """
        self.data = data
        self.fig = None
    
    def create_dashboard(self) -> go.Figure:
        """
        Създаване на цялостен dashboard с multiple charts
        
        Returns:
            Plotly Figure обект
        """
        # Създаване на subplot grid (2x2)
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Топ 10 Марки по Пазарен Дял',
                'Разпределение на Цени по Категория',
                'Средна Цена vs Среден Рейтинг',
                'Разпределение на Продукти по Ценова Категория'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'box'}],
                [{'type': 'scatter'}, {'type': 'pie'}]
            ]
        )
        
        # Chart 1: Топ марки
        brand_counts = self.data['brand'].value_counts().head(10)
        fig.add_trace(
            go.Bar(
                x=brand_counts.index,
                y=brand_counts.values,
                name='Брой продукти',
                marker_color='#1f77b4'
            ),
            row=1, col=1
        )
        
        # Chart 2: Box plot на цени по категория
        for category in self.data['category'].unique()[:5]:
            category_data = self.data[self.data['category'] == category]['price']
            fig.add_trace(
                go.Box(
                    y=category_data,
                    name=category,
                    boxmean='sd'
                ),
                row=1, col=2
            )
        
        # Chart 3: Scatter plot - цена vs рейтинг
        brand_agg = self.data.groupby('brand').agg({
            'price': 'mean',
            'rating': 'mean',
            'asin': 'count'
        }).reset_index()
        brand_agg.columns = ['brand', 'avg_price', 'avg_rating', 'product_count']
        
        fig.add_trace(
            go.Scatter(
                x=brand_agg['avg_price'],
                y=brand_agg['avg_rating'],
                mode='markers',
                marker=dict(
                    size=brand_agg['product_count'] / 2,
                    color=brand_agg['avg_rating'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Рейтинг")
                ),
                text=brand_agg['brand'],
                hovertemplate='<b>%{text}</b><br>Цена: $%{x:.2f}<br>Рейтинг: %{y:.2f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Chart 4: Pie chart - ценови категории
        price_category_counts = self.data['price_category'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=price_category_counts.index,
                values=price_category_counts.values,
                hole=0.3
            ),
            row=2, col=2
        )
        
        # Layout настройки
        fig.update_layout(
            title_text="<b>Amazon Brand Analytics - Sales Dashboard</b>",
            title_font_size=20,
            showlegend=False,
            height=900,
            width=1400
        )
        
        fig.update_xaxes(title_text="Марка", row=1, col=1)
        fig.update_yaxes(title_text="Брой продукти", row=1, col=1)
        
        fig.update_xaxes(title_text="Категория", row=1, col=2)
        fig.update_yaxes(title_text="Цена ($)", row=1, col=2)
        
        fig.update_xaxes(title_text="Средна цена ($)", row=2, col=1)
        fig.update_yaxes(title_text="Среден рейтинг", row=2, col=1)
        
        self.fig = fig
        return fig
    
    def create_kpi_cards(self) -> Dict:
        """
        Генериране на KPI метрики
        
        Returns:
            Речник с KPI стойности
        """
        kpis = {
            'total_products': len(self.data),
            'total_brands': self.data['brand'].nunique(),
            'avg_price': self.data['price'].mean(),
            'avg_rating': self.data['rating'].mean(),
            'total_reviews': self.data['reviews_count'].sum(),
            'categories': self.data['category'].nunique()
        }
        
        return kpis
    
    def save_dashboard(self, filename: str = 'sales_dashboard.html'):
        """
        Запазване на dashboard като HTML
        
        Args:
            filename: Име на изходния файл
        """
        if self.fig is None:
            self.create_dashboard()
        
        self.fig.write_html(filename)
        print(f"✓ Dashboard запазен в {filename}")
    
    def show_dashboard(self):
        """Показване на dashboard в browser"""
        if self.fig is None:
            self.create_dashboard()
        
        self.fig.show()


def main():
    """Тестване на dashboard"""
    # Зареждане на данни
    data = pd.read_csv('amazon_products_clean.csv')
    
    # Създаване на dashboard
    dashboard = SalesDashboard(data)
    
    # Генериране и запазване
    dashboard.create_dashboard()
    dashboard.save_dashboard()
    
    # KPI метрики
    kpis = dashboard.create_kpi_cards()
    print("\nKPI Метрики:")
    print(f"Общо продукти: {kpis['total_products']:,}")
    print(f"Брой марки: {kpis['total_brands']}")
    print(f"Средна цена: ${kpis['avg_price']:.2f}")
    print(f"Среден рейтинг: {kpis['avg_rating']:.2f}")


if __name__ == '__main__':
    main()
