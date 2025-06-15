"""
Dashboard Analytics Engine
Real-time metrics calculation and trend analysis for brand analytics
"""
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import statistics

logger = logging.getLogger(__name__)


class DashboardEngine:
    """
    Engine for calculating real-time analytics metrics.
    Provides trend analysis and data preparation for visualization.
    """
    
    def __init__(self, db_manager=None, cache_manager=None):
        self.db = db_manager
        self.cache = cache_manager
        logger.info("DashboardEngine initialized")
    
    def calculate_brand_metrics(self, brand_id: int, 
                                  date_range_days: int = 30) -> Dict:
        """
        Calculate comprehensive brand performance metrics.
        
        Args:
            brand_id: Brand identifier
            date_range_days: Number of days to analyze
            
        Returns:
            dict with all brand metrics
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=date_range_days)
        
        metrics = {
            'brand_id': brand_id,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat(),
                'days': date_range_days
            },
            'visibility_score': self._calculate_visibility(brand_id),
            'keyword_rankings': self._get_keyword_rankings(brand_id),
            'sales_metrics': self._get_sales_metrics(brand_id),
            'trend_data': self._calculate_trends(brand_id, date_range_days),
            'competitor_position': self._get_competitor_position(brand_id),
            'calculated_at': datetime.now().isoformat()
        }
        
        return metrics
    
    def _calculate_visibility(self, brand_id: int) -> Dict:
        """Calculate brand visibility score"""
        return {
            'score': 0.0,
            'change': 0.0,
            'trend': 'stable',
            'components': {
                'search_presence': 0.0,
                'ranking_strength': 0.0,
                'keyword_coverage': 0.0
            }
        }
    
    def _get_keyword_rankings(self, brand_id: int) -> Dict:
        """Get keyword ranking summary"""
        return {
            'total_keywords': 0,
            'top_10_count': 0,
            'top_50_count': 0,
            'average_position': 0.0,
            'keywords': []
        }
    
    def _get_sales_metrics(self, brand_id: int) -> Dict:
        """Get sales performance metrics"""
        return {
            'estimated_revenue': 0.0,
            'units_sold': 0,
            'conversion_rate': 0.0,
            'average_order_value': 0.0
        }
    
    def _calculate_trends(self, brand_id: int, days: int) -> List[Dict]:
        """Calculate trend data points for visualization"""
        trend_data = []
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            trend_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'visibility_score': 0.0,
                'keyword_count': 0,
                'ranking_average': 0.0
            })
        return trend_data
    
    def _get_competitor_position(self, brand_id: int) -> Dict:
        """Get brand position relative to competitors"""
        return {
            'market_rank': 0,
            'market_share': 0.0,
            'competitors_above': 0,
            'competitors_below': 0
        }
    
    def prepare_chart_data(self, metrics: Dict, chart_type: str) -> Dict:
        """
        Prepare data in format suitable for Chart.js visualization.
        
        Args:
            metrics: Raw metrics data
            chart_type: Type of chart (line, bar, pie, etc.)
            
        Returns:
            Chart.js compatible data structure
        """
        if chart_type == 'line':
            trend_data = metrics.get('trend_data', [])
            return {
                'labels': [d['date'] for d in trend_data],
                'datasets': [{
                    'label': 'Visibility Score',
                    'data': [d['visibility_score'] for d in trend_data],
                    'borderColor': '#4F46E5',
                    'backgroundColor': 'rgba(79, 70, 229, 0.1)',
                    'fill': True,
                    'tension': 0.4
                }]
            }
        
        elif chart_type == 'bar':
            return {
                'labels': [],
                'datasets': [{
                    'label': 'Keyword Rankings',
                    'data': [],
                    'backgroundColor': '#10B981'
                }]
            }
        
        elif chart_type == 'pie':
            return {
                'labels': [],
                'datasets': [{
                    'data': [],
                    'backgroundColor': ['#4F46E5', '#10B981', '#F59E0B', '#EF4444']
                }]
            }
        
        return {}
    
    def generate_actionable_insights(self, metrics: Dict) -> List[Dict]:
        """
        Generate actionable insights from metrics data.
        
        Returns:
            List of insight objects with recommendations
        """
        insights = []
        
        visibility = metrics.get('visibility_score', {})
        if visibility.get('score', 0) < 30:
            insights.append({
                'type': 'warning',
                'category': 'visibility',
                'message': 'Brand visibility is low. Consider optimizing product listings.',
                'priority': 'high',
                'action': 'Review and update product titles, descriptions, and keywords'
            })
        
        rankings = metrics.get('keyword_rankings', {})
        if rankings.get('average_position', 0) > 50:
            insights.append({
                'type': 'warning',
                'category': 'rankings',
                'message': 'Average keyword position is beyond page 5. SEO improvements needed.',
                'priority': 'high',
                'action': 'Focus on high-volume, low-competition keywords'
            })
        
        return insights
