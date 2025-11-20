# -*- coding: utf-8 -*-
"""
=============================================================================
CONFTEST - E2E Test Configuration
=============================================================================
Автор: Цвета Попова
Дата: 10 Декември 2025
Цел: Pytest fixtures за E2E тестове
=============================================================================
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver():
    """Selenium WebDriver fixture"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    """Base URL fixture"""
    return 'http://localhost:3000'


@pytest.fixture(scope="session")
def api_base_url():
    """API Base URL fixture"""
    return 'http://localhost:5000/api/v1'
