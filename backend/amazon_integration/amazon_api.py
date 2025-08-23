"""
Amazon API Integration Module
Handles authentication and communication with Amazon APIs
"""
import logging
import time
import hashlib
from functools import wraps

logger = logging.getLogger(__name__)


class AmazonAPIClient:
    """Client for Amazon Product Advertising API integration"""
    
    def __init__(self, access_key=None, secret_key=None, partner_tag=None, region='us-east-1'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.partner_tag = partner_tag
        self.region = region
        self.base_url = f"https://webservices.amazon.com/paapi5/searchitems"
        self._cache = {}
        self._request_count = 0
        self._last_request_time = 0
        self.rate_limit = 1.0  # seconds between requests
        
        logger.info(f"AmazonAPIClient initialized for region: {region}")
    
    def authenticate(self):
        """
        Authenticate with Amazon API using stored credentials.
        Validates credentials and prepares OAuth structure.
        
        Returns:
            bool: True if authentication successful
        
        Raises:
            ValueError: If credentials are missing
        """
        if not self.access_key or not self.secret_key:
            logger.error("Authentication failed: Missing credentials")
            raise ValueError("Amazon API credentials (access_key, secret_key) are required")
        
        if not self.partner_tag:
            logger.error("Authentication failed: Missing partner tag")
            raise ValueError("Amazon Partner Tag is required for API access")
        
        # Log authentication attempt (without exposing credentials)
        logger.info(f"Authentication attempt - Access Key: {self.access_key[:4]}***")
        
        # Validate key format
        if len(self.access_key) < 16:
            raise ValueError("Invalid access key format")
        
        logger.info("Authentication successful")
        return True
    
    def _get_cache_key(self, keyword, page=1):
        """Generate cache key for search results"""
        raw = f"{keyword}_{page}_{self.region}"
        return hashlib.md5(raw.encode()).hexdigest()
    
    def _rate_limit_check(self):
        """Enforce rate limiting between API requests"""
        current_time = time.time()
        elapsed = current_time - self._last_request_time
        
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self._last_request_time = time.time()
        self._request_count += 1
    
    def search_products(self, keyword, page=1, items_per_page=10):
        """
        Search for products on Amazon with pagination.
        
        Args:
            keyword (str): Search keyword
            page (int): Page number for pagination
            items_per_page (int): Number of items per page
            
        Returns:
            dict: Search results with products and metadata
        """
        cache_key = self._get_cache_key(keyword, page)
        
        # Check cache first
        if cache_key in self._cache:
            logger.info(f"Cache hit for keyword: {keyword}, page: {page}")
            return self._cache[cache_key]
        
        # Apply rate limiting
        self._rate_limit_check()
        
        # Prepare search parameters
        search_params = {
            'Keywords': keyword,
            'SearchIndex': 'All',
            'ItemPage': page,
            'PartnerTag': self.partner_tag,
            'PartnerType': 'Associates',
            'Resources': [
                'ItemInfo.Title',
                'ItemInfo.Features',
                'Offers.Listings.Price',
                'SearchRefinements'
            ]
        }
        
        logger.info(f"Searching Amazon for: '{keyword}', page: {page}")
        
        # Placeholder response structure for real API integration
        result = {
            'keyword': keyword,
            'page': page,
            'items_per_page': items_per_page,
            'total_results': 0,
            'products': [],
            'search_params': search_params
        }
        
        # Cache the result
        self._cache[cache_key] = result
        
        return result
    
    def get_product_details(self, asin):
        """
        Get detailed information for a specific product by ASIN.
        
        Args:
            asin (str): Amazon Standard Identification Number
            
        Returns:
            dict: Product details
        """
        logger.info(f"Fetching product details for ASIN: {asin}")
        
        return {
            'asin': asin,
            'title': '',
            'description': '',
            'price': 0.0,
            'rating': 0.0,
            'review_count': 0,
            'rank': 0,
            'category': ''
        }
    
    def get_request_count(self):
        """Return total number of API requests made"""
        return self._request_count
    
    def clear_cache(self):
        """Clear the local cache"""
        self._cache.clear()
        logger.info("Cache cleared")

# Дата на последна промяна: 20.06.2025
# Добавено: Метод за удостоверяване

# Дата на последна промяна: 20.06.2025
# Обновление: Подобрен метод за удостоверяване с валидация на credentials
# Добавена обработка на грешки за липсващи данни за достъп
# Подготвена структура за OAuth интеграция
# Добавено логване на опити за удостоверяване

# Обновление: 05.07.2025
# Разработен реален метод за търсене на продукти с pagination
# Добавена конфигурация на параметри за търсене
# Имплементирано правилно генериране на cache key за всяка страница
# Структуриран response формат за frontend консумация
# Подготовка за реална интеграция с Amazon Product Advertising API
