"""
Модул за Анализ на Данни
Обработва данни от Amazon и генерира прозрения
Автор: Диана Георгиева (с архитектура от Мартин Дачев)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict

class BrandAnalyzer:
    """
    Анализатор за показатели на представяне на брандове
    """
    
    def __init__(self):
        """Инициализира анализатора"""
        self.data = None
    
    def analyze_keyword_performance(self, keyword_data: List[Dict]) -> Dict:
        """
        Анализира представяне на ключови думи във времето
        
        Args:
            keyword_data: Списък със записи за класиране на ключови думи
            
        Returns:
            Dict с резултати от анализа
        """
        if not keyword_data:
            return {
                'грешка': 'Не са предоставени данни',
                'показатели': {}
            }
        
        # Преобразувай в DataFrame за анализ
        df = pd.DataFrame(keyword_data)
        
        # Изчисли показатели
        metrics = {
            'средна_позиция': df['позиция'].mean() if 'позиция' in df else 0,
            'най_добра_позиция': df['позиция'].min() if 'позиция' in df else 0,
            'най_лоша_позиция': df['позиция'].max() if 'позиция' in df else 0,
            'тенденция_на_позиция': self._calculate_trend(df['позиция'].tolist()) if 'позиция' in df else 0,
            'общо_ключови_думи': len(df),
            'времеви_печат': datetime.now().isoformat()
        }
        
        return {
            'показатели': metrics,
            'препоръки': self._generate_recommendations(metrics)
        }
    
    def compare_competitors(self, brand_data: Dict, competitor_data: List[Dict]) -> Dict:
        """
        Сравни представяне на бранд спрямо конкуренти
        
        Args:
            brand_data: Данни за представяне на бранда
            competitor_data: Списък с данни за представяне на конкуренти
            
        Returns:
            Dict с резултати от сравнението
        """
        # TODO: Имплементирай логика за сравнение на конкуренти
        return {
            'позиция_на_бранд': brand_data.get('средна_позиция', 0),
            'конкуренти': [],
            'пазарен_дял': 0.0,
            'препоръки': []
        }
    
    def calculate_visibility_score(self, rankings: List[Dict]) -> float:
        """
        Изчисли показател за видимост на бранд (0-100)
        
        Args:
            rankings: Списък със записи за класиране
            
        Returns:
            Показател за видимост
        """
        if not rankings:
            return 0.0
        
        # Претеглено оценяване: по-високи позиции = по-висок резултат
        total_score = 0
        for ranking in rankings:
            position = ranking.get('позиция', 100)
            # Позиция 1 = 100 точки, позиция 20 = 5 точки
            score = max(0, 100 - (position - 1) * 5)
            total_score += score
        
        # Среден резултат
        return round(total_score / len(rankings), 2)
    
    def detect_product_position(self, search_results: List[Dict], target_asin: str) -> Optional[Dict]:
        """
        Открий позицията на конкретен продукт в резултатите от търсене
        
        Args:
            search_results: Списък с резултати от търсене на продукти
            target_asin: ASIN на продукта за намиране
            
        Returns:
            Dict с информация за позицията или None ако не е намерен
        """
        for index, product in enumerate(search_results):
            if product.get('asin') == target_asin:
                position = index + 1
                page = (position - 1) // 20 + 1
                position_on_page = ((position - 1) % 20) + 1
                
                return {
                    'asin': target_asin,
                    'обща_позиция': position,
                    'страница': page,
                    'позиция_на_страница': position_on_page,
                    'спонсорирана': product.get('спонсорирана', False),
                    'времеви_печат': datetime.now().isoformat()
                }
        
        return None
    
    def track_ranking_changes(self, current_rankings: List[Dict], 
                             previous_rankings: List[Dict]) -> Dict:
        """
        Сравни текущи и предишни класирания за откриване на промени
        
        Args:
            current_rankings: Текущи данни за класиране
            previous_rankings: Предишни данни за класиране
            
        Returns:
            Dict с анализ на промените в класирането
        """
        changes = []
        
        for current in current_rankings:
            asin = current.get('asin')
            keyword = current.get('ключова_дума')
            current_pos = current.get('позиция')
            
            # Намери предишно класиране за същия ASIN и ключова дума
            previous = next(
                (p for p in previous_rankings 
                 if p.get('asin') == asin and p.get('ключова_дума') == keyword),
                None
            )
            
            if previous:
                previous_pos = previous.get('позиция')
                change = previous_pos - current_pos  # Положително = подобрение
                
                changes.append({
                    'asin': asin,
                    'ключова_дума': keyword,
                    'текуща_позиция': current_pos,
                    'предишна_позиция': previous_pos,
                    'промяна': change,
                    'тенденция': 'подобрение' if change > 0 else 'влошаване' if change < 0 else 'стабилно'
                })
        
        return {
            'промени': changes,
            'общо_проследени': len(changes),
            'подобрения': len([c for c in changes if c['промяна'] > 0]),
            'влошавания': len([c for c in changes if c['промяна'] < 0]),
            'времеви_печат': datetime.now().isoformat()
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """
        Изчисли посока на тенденция
        
        Args:
            values: Списък с числови стойности във времето
            
        Returns:
            Посока на тенденция: 'подобрение', 'стабилно', 'влошаване'
        """
        if len(values) < 2:
            return 'стабилно'
        
        # Проста линейна регресия
        x = np.arange(len(values))
        y = np.array(values)
        slope = np.polyfit(x, y, 1)[0]
        
        # За класирания, отрицателен наклон = подобрение (по-ниско число на позиция)
        if slope < -0.5:
            return 'подобрение'
        elif slope > 0.5:
            return 'влошаване'
        else:
            return 'стабилно'
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """
        Генерира препоръки за оптимизация базирани на показателите
        
        Args:
            metrics: Показатели за представяне
            
        Returns:
            Списък с препоръки
        """
        recommendations = []
        
        avg_pos = metrics.get('средна_позиция', 100)
        trend = metrics.get('тенденция_на_позиция', 'стабилно')
        
        if avg_pos > 20:
            recommendations.append(
                "Средната позиция е под първа страница. Разгледайте подобряване на SEO и увеличаване на разходите за реклама."
            )
        
        if trend == 'влошаване':
            recommendations.append(
                "Класиранията се влошават. Прегледайте стратегиите на конкурентите и актуализирайте описанията на продуктите."
            )
        
        if trend == 'подобрение':
            recommendations.append(
                "Класиранията се подобряват. Продължете текущите стратегии за оптимизация."
            )
        
        return recommendations
