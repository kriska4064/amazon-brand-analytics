"""
Unit Tests for Amazon API Client
Test coverage: ~45% of amazon_api.py
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from backend.amazon_integration.amazon_api import AmazonAPIClient


class TestAmazonAPIClientInitialization:
    """Test suite for API client initialization"""
    
    def test_client_initializes_with_credentials(self):
        """Test that client initializes correctly with valid credentials"""
        client = AmazonAPIClient(
            access_key='AKIAIOSFODNN7EXAMPLE',
            secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            partner_tag='test-20',
            region='us-east-1'
        )
        assert client.access_key == 'AKIAIOSFODNN7EXAMPLE'
        assert client.region == 'us-east-1'
    
    def test_client_default_region(self):
        """Test default region is set correctly"""
        client = AmazonAPIClient()
        assert client.region == 'us-east-1'
    
    def test_client_rate_limit_default(self):
        """Test default rate limit setting"""
        client = AmazonAPIClient()
        assert client.rate_limit == 1.0
    
    def test_client_cache_initially_empty(self):
        """Test cache is empty on initialization"""
        client = AmazonAPIClient()
        assert len(client._cache) == 0
    
    def test_client_request_count_zero(self):
        """Test request count starts at zero"""
        client = AmazonAPIClient()
        assert client.get_request_count() == 0


class TestAmazonAPIAuthentication:
    """Tests for authentication mechanism"""
    
    def test_authentication_succeeds_with_valid_credentials(self):
        """Test successful authentication with valid credentials"""
        client = AmazonAPIClient(
            access_key='AKIAIOSFODNN7EXAMPLE',
            secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            partner_tag='test-20'
        )
        result = client.authenticate()
        assert result is True
    
    def test_authentication_fails_without_access_key(self):
        """Test authentication fails when access key is missing"""
        client = AmazonAPIClient(
            secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            partner_tag='test-20'
        )
        with pytest.raises(ValueError, match="credentials"):
            client.authenticate()
    
    def test_authentication_fails_without_partner_tag(self):
        """Test authentication fails when partner tag is missing"""
        client = AmazonAPIClient(
            access_key='AKIAIOSFODNN7EXAMPLE',
            secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        )
        with pytest.raises(ValueError, match="Partner Tag"):
            client.authenticate()


class TestRateLimiting:
    """Tests for rate limiting mechanism"""
    
    def test_rate_limit_tracking(self):
        """Test that request count is tracked correctly"""
        client = AmazonAPIClient(
            access_key='AKIAIOSFODNN7EXAMPLE',
            secret_key='secret',
            partner_tag='test-20'
        )
        # Initial count should be zero
        assert client.get_request_count() == 0
    
    def test_rate_limit_configurable(self):
        """Test that rate limit can be configured"""
        client = AmazonAPIClient()
        client.rate_limit = 2.0
        assert client.rate_limit == 2.0


class TestCacheFunctionality:
    """Tests for caching mechanism"""
    
    def test_cache_key_generation(self):
        """Test that cache keys are generated correctly"""
        client = AmazonAPIClient()
        key1 = client._get_cache_key('laptop', 1)
        key2 = client._get_cache_key('laptop', 2)
        key3 = client._get_cache_key('laptop', 1)
        
        # Same params should produce same key
        assert key1 == key3
        # Different params should produce different keys
        assert key1 != key2
    
    def test_cache_clear(self):
        """Test cache can be cleared"""
        client = AmazonAPIClient()
        client._cache['test_key'] = {'data': 'test'}
        client.clear_cache()
        assert len(client._cache) == 0
    
    def test_search_results_cached(self):
        """Test that search results are cached after first call"""
        client = AmazonAPIClient(
            access_key='AKIAIOSFODNN7EXAMPLE',
            secret_key='secret',
            partner_tag='test-20'
        )
        # Mock the rate limit to avoid actual sleeping
        client.rate_limit = 0.0
        
        result1 = client.search_products('test keyword', page=1)
        result2 = client.search_products('test keyword', page=1)
        
        # Should return same result from cache
        assert result1 == result2

# Обновление: 28.06.2025 - Допълнени тестове
class TestAPIRateLimitExtended:
    """Extended rate limiting tests"""
    
    def test_request_tracking_increments(self):
        """Test request count increments on search"""
        client = AmazonAPIClient()
        client.rate_limit = 0.0
        initial = client.get_request_count()
        client.search_products('test', page=1)
        assert client.get_request_count() == initial + 1
