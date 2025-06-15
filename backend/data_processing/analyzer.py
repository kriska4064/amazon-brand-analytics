"""
Data Analyzer Module
Handles keyword ranking detection, tracking and competitor analysis
"""
import logging
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class KeywordRankAnalyzer:
    """
    Analyzes keyword rankings for Amazon products.
    Detects position in search results and tracks changes over time.
    """
    
    def __init__(self):
        self.ranking_history = {}
        logger.info("KeywordRankAnalyzer initialized")
    
    def detect_product_position(self, search_results: List[Dict], target_asin: str) -> Optional[int]:
        """
        Detect the position of a product in search results.
        
        Args:
            search_results: List of products from search
            target_asin: The ASIN to find
            
        Returns:
            Position (1-indexed) or None if not found
        """
        for idx, product in enumerate(search_results, 1):
            if product.get('asin') == target_asin:
                logger.info(f"Product {target_asin} found at position {idx}")
                return idx
        
        logger.info(f"Product {target_asin} not found in search results")
        return None
    
    def track_ranking_changes(self, keyword: str, asin: str, 
                               current_position: int, 
                               previous_position: Optional[int] = None) -> Dict:
        """
        Track changes in ranking between periods.
        
        Returns:
            dict with improvement/decline data
        """
        change = 0
        trend = 'stable'
        
        if previous_position is not None and current_position is not None:
            # Lower position number = better ranking
            change = previous_position - current_position
            if change > 0:
                trend = 'improved'
            elif change < 0:
                trend = 'declined'
        
        # Store in history
        history_key = f"{keyword}_{asin}"
        if history_key not in self.ranking_history:
            self.ranking_history[history_key] = []
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'position': current_position,
            'change': change,
            'trend': trend
        }
        self.ranking_history[history_key].append(entry)
        
        logger.info(f"Ranking tracked - Keyword: {keyword}, ASIN: {asin}, "
                   f"Position: {current_position}, Trend: {trend}")
        
        return {
            'keyword': keyword,
            'asin': asin,
            'current_position': current_position,
            'previous_position': previous_position,
            'change': change,
            'trend': trend,
            'improvements': max(0, change),
            'declines': max(0, -change)
        }
    
    def analyze_trends(self, keyword: str, asin: str, periods: int = 7) -> Dict:
        """
        Analyze ranking trends for dashboard visualization.
        
        Args:
            keyword: Search keyword
            asin: Product ASIN
            periods: Number of periods to analyze
            
        Returns:
            Trend analysis data for visualization
        """
        history_key = f"{keyword}_{asin}"
        history = self.ranking_history.get(history_key, [])
        
        if not history:
            return {
                'keyword': keyword,
                'asin': asin,
                'trend': 'no_data',
                'data_points': []
            }
        
        recent = history[-periods:] if len(history) >= periods else history
        
        positions = [entry['position'] for entry in recent if entry['position'] is not None]
        
        if len(positions) >= 2:
            avg_improvement = sum(
                recent[i]['change'] for i in range(1, len(recent))
            ) / (len(recent) - 1)
            overall_trend = 'improved' if avg_improvement > 0 else \
                           'declined' if avg_improvement < 0 else 'stable'
        else:
            overall_trend = 'insufficient_data'
        
        return {
            'keyword': keyword,
            'asin': asin,
            'trend': overall_trend,
            'data_points': recent,
            'best_position': min(positions) if positions else None,
            'worst_position': max(positions) if positions else None,
            'average_position': sum(positions) / len(positions) if positions else None
        }


class CompetitorAnalyzer:
    """
    Analyzes competitor brands and products on Amazon.
    Detects competitors, calculates market share and compares rankings.
    """
    
    def __init__(self):
        self.competitor_data = {}
        logger.info("CompetitorAnalyzer initialized")
    
    def detect_competitors(self, search_results: List[Dict], 
                           target_brand: str, top_n: int = 5) -> List[Dict]:
        """
        Detect competitor brands in search results.
        
        Args:
            search_results: Products from Amazon search
            target_brand: The brand we're analyzing
            top_n: Number of top competitors to return
            
        Returns:
            List of competitor brands with data
        """
        brand_counts = {}
        brand_positions = {}
        
        for idx, product in enumerate(search_results, 1):
            brand = product.get('brand', 'Unknown')
            if brand == target_brand:
                continue
            
            if brand not in brand_counts:
                brand_counts[brand] = 0
                brand_positions[brand] = []
            
            brand_counts[brand] += 1
            brand_positions[brand].append(idx)
        
        competitors = []
        for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]:
            avg_position = sum(brand_positions[brand]) / len(brand_positions[brand])
            competitors.append({
                'brand': brand,
                'product_count': count,
                'average_position': avg_position,
                'best_position': min(brand_positions[brand])
            })
        
        logger.info(f"Detected {len(competitors)} competitors for brand: {target_brand}")
        return competitors
    
    def calculate_market_share(self, search_results: List[Dict]) -> Dict:
        """
        Calculate market share based on search result presence.
        
        Returns:
            dict with brand -> market share percentage
        """
        total = len(search_results)
        if total == 0:
            return {}
        
        brand_counts = {}
        for product in search_results:
            brand = product.get('brand', 'Unknown')
            brand_counts[brand] = brand_counts.get(brand, 0) + 1
        
        market_share = {
            brand: (count / total) * 100 
            for brand, count in brand_counts.items()
        }
        
        return dict(sorted(market_share.items(), key=lambda x: x[1], reverse=True))
    
    def compare_rankings(self, target_brand: str, 
                         competitors: List[Dict],
                         keyword: str) -> Dict:
        """
        Compare rankings between target brand and competitors.
        
        Returns:
            Comparison data for dashboard visualization
        """
        comparison = {
            'keyword': keyword,
            'target_brand': target_brand,
            'competitors': competitors,
            'ranking_comparison': [],
            'timestamp': datetime.now().isoformat()
        }
        
        for comp in competitors:
            comparison['ranking_comparison'].append({
                'brand': comp['brand'],
                'average_position': comp['average_position'],
                'best_position': comp['best_position'],
                'product_count': comp['product_count']
            })
        
        return comparison
