"""
Brand and Product Data Models
"""
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Brand:
    """Brand data model with CRUD operations"""
    
    def __init__(self, brand_id=None, name=None, amazon_store_id=None,
                 description=None, category=None, created_at=None):
        self.id = brand_id
        self.name = name
        self.amazon_store_id = amazon_store_id
        self.description = description
        self.category = category
        self.created_at = created_at or datetime.now()
        self.products = []
        self.keywords = []
        self.visibility_score = 0.0
    
    @classmethod
    def create(cls, name, amazon_store_id, description=None, category=None):
        """Create a new brand instance"""
        brand = cls(
            name=name,
            amazon_store_id=amazon_store_id,
            description=description,
            category=category
        )
        logger.info(f"Brand created: {name}")
        return brand
    
    def update(self, **kwargs):
        """Update brand attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        logger.info(f"Brand updated: {self.name}")
        return self
    
    def delete(self):
        """Mark brand as deleted"""
        logger.info(f"Brand deleted: {self.name}")
        return True
    
    def to_dict(self):
        """Serialize brand to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'amazon_store_id': self.amazon_store_id,
            'description': self.description,
            'category': self.category,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'visibility_score': self.visibility_score,
            'product_count': len(self.products),
            'keyword_count': len(self.keywords)
        }
    
    def __repr__(self):
        return f"<Brand id={self.id} name='{self.name}'>"


class Product:
    """Product data model with Amazon-specific fields"""
    
    def __init__(self, asin=None, title=None, brand_id=None,
                 price=None, rating=None, review_count=None,
                 rank=None, category=None, created_at=None):
        self.asin = asin
        self.title = title
        self.brand_id = brand_id
        self.price = price or 0.0
        self.rating = rating or 0.0
        self.review_count = review_count or 0
        self.rank = rank
        self.category = category
        self.created_at = created_at or datetime.now()
        self.keywords = []
        self.ranking_history = []
    
    @classmethod
    def from_amazon_response(cls, amazon_data):
        """Create Product from Amazon API response"""
        return cls(
            asin=amazon_data.get('ASIN'),
            title=amazon_data.get('ItemInfo', {}).get('Title', {}).get('DisplayValue', ''),
            price=amazon_data.get('Offers', {}).get('Listings', [{}])[0].get('Price', {}).get('Amount', 0.0),
            rating=amazon_data.get('CustomerReviews', {}).get('StarRating', {}).get('Value', 0.0),
            review_count=amazon_data.get('CustomerReviews', {}).get('Count', 0)
        )
    
    def update_rank(self, new_rank):
        """Update product rank and store in history"""
        old_rank = self.rank
        self.rank = new_rank
        self.ranking_history.append({
            'timestamp': datetime.now().isoformat(),
            'rank': new_rank,
            'previous_rank': old_rank
        })
        return self
    
    def to_dict(self):
        """Serialize product to dictionary"""
        return {
            'asin': self.asin,
            'title': self.title,
            'brand_id': self.brand_id,
            'price': self.price,
            'rating': self.rating,
            'review_count': self.review_count,
            'rank': self.rank,
            'category': self.category,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'keyword_count': len(self.keywords)
        }
    
    def __repr__(self):
        return f"<Product asin='{self.asin}' title='{self.title[:30]}...'>"

# Обновление: 19.07.2025
# Имплементиран Brand модел с CRUD операции
# Създаден Product модел с Amazon-специфични полета
# Добавени методи за сериализация в dictionary
# Подготовка за database ORM интеграция
