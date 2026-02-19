# -*- coding: utf-8 -*-
"""
=============================================================================
END-TO-END TESTS - User Journey
=============================================================================
Автор: Цвета Попова
Дата: 10 Декември 2025
Цел: E2E тестове симулиращи реални потребителски сценарии
=============================================================================
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


class TestUserJourney(unittest.TestCase):
    """E2E тестове за потребителски пътища"""
    
    @classmethod
    def setUpClass(cls):
        """Setup преди всички тестове"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Headless режим
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.base_url = 'http://localhost:3000'
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup след всички тестове"""
        cls.driver.quit()
    
    def test_01_user_login(self):
        """Тест: Потребителско влизане"""
        driver = self.driver
        driver.get(f'{self.base_url}/login')
        
        # Намиране на полета за вход
        username_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.ID, 'login-btn')
        
        # Попълване на данни
        username_field.send_keys('test_user')
        password_field.send_keys('test_password')
        login_button.click()
        
        # Проверка за успешно влизане
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'dashboard'))
        )
        
        self.assertIn('dashboard', driver.current_url)
        print("✓ Потребителят успешно се вписа")
    
    def test_02_search_products(self):
        """Тест: Търсене на продукти"""
        driver = self.driver
        driver.get(f'{self.base_url}/dashboard')
        
        # Намиране на search bar
        search_box = driver.find_element(By.ID, 'search-box')
        search_button = driver.find_element(By.ID, 'search-btn')
        
        # Търсене на продукти от марка Amazon
        search_box.send_keys('Amazon Echo')
        search_button.click()
        
        # Изчакване на резултати
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-card'))
        )
        
        # Проверка на резултатите
        products = driver.find_elements(By.CLASS_NAME, 'product-card')
        self.assertGreater(len(products), 0)
        print(f"✓ Намерени {len(products)} продукта")
    
    def test_03_view_product_details(self):
        """Тест: Преглед на детайли за продукт"""
        driver = self.driver
        
        # Кликване на първия продукт от резултатите
        first_product = driver.find_element(By.CLASS_NAME, 'product-card')
        first_product.click()
        
        # Изчакване на страницата с детайли
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'product-details'))
        )
        
        # Проверка на елементи
        title = driver.find_element(By.CLASS_NAME, 'product-title')
        price = driver.find_element(By.CLASS_NAME, 'product-price')
        rating = driver.find_element(By.CLASS_NAME, 'product-rating')
        
        self.assertIsNotNone(title.text)
        self.assertIsNotNone(price.text)
        print(f"✓ Детайли за продукт: {title.text}, Цена: {price.text}")
    
    def test_04_view_price_history_chart(self):
        """Тест: Преглед на графика с ценова история"""
        driver = self.driver
        
        # Намиране на бутон за price history
        price_history_btn = driver.find_element(By.ID, 'price-history-btn')
        price_history_btn.click()
        
        # Изчакване на зареждане на графиката
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'price-chart'))
        )
        
        # Проверка дали графиката се показва
        chart = driver.find_element(By.ID, 'price-chart')
        self.assertTrue(chart.is_displayed())
        print("✓ Графика с ценова история се показва коректно")
    
    def test_05_filter_by_price_range(self):
        """Тест: Филтриране по ценови диапазон"""
        driver = self.driver
        driver.get(f'{self.base_url}/dashboard')
        
        # Намиране на филтри
        min_price_input = driver.find_element(By.ID, 'min-price')
        max_price_input = driver.find_element(By.ID, 'max-price')
        apply_filter_btn = driver.find_element(By.ID, 'apply-filter-btn')
        
        # Задаване на ценови диапазон
        min_price_input.send_keys('20')
        max_price_input.send_keys('50')
        apply_filter_btn.click()
        
        # Изчакване на филтрирани резултати
        time.sleep(2)
        
        # Проверка на цените в резултатите
        products = driver.find_elements(By.CLASS_NAME, 'product-card')
        self.assertGreater(len(products), 0)
        print(f"✓ Филтрирани {len(products)} продукта в диапазон 20-50")
    
    def test_06_add_to_watchlist(self):
        """Тест: Добавяне на продукт към watchlist"""
        driver = self.driver
        
        # Намиране на бутон за watchlist
        watchlist_btn = driver.find_element(By.CLASS_NAME, 'add-to-watchlist-btn')
        watchlist_btn.click()
        
        # Изчакване на потвърждение
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'success-message'))
        )
        
        success_msg = driver.find_element(By.CLASS_NAME, 'success-message')
        self.assertIn('Добавен към watchlist', success_msg.text)
        print("✓ Продукт добавен към watchlist")
    
    def test_07_generate_report(self):
        """Тест: Генериране на отчет"""
        driver = self.driver
        driver.get(f'{self.base_url}/reports')
        
        # Избор на тип отчет
        report_type = driver.find_element(By.ID, 'report-type')
        report_type.click()
        
        # Избор на "Price Analysis"
        price_analysis_option = driver.find_element(By.XPATH, "//option[@value='price_analysis']")
        price_analysis_option.click()
        
        # Генериране на отчет
        generate_btn = driver.find_element(By.ID, 'generate-report-btn')
        generate_btn.click()
        
        # Изчакване на генериране
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'report-preview'))
        )
        
        report_preview = driver.find_element(By.ID, 'report-preview')
        self.assertTrue(report_preview.is_displayed())
        print("✓ Отчет генериран успешно")
    
    def test_08_user_logout(self):
        """Тест: Излизане на потребител"""
        driver = self.driver
        
        # Намиране на logout бутон
        logout_btn = driver.find_element(By.ID, 'logout-btn')
        logout_btn.click()
        
        # Изчакване на redirect към login страница
        WebDriverWait(driver, 5).until(
            EC.url_contains('login')
        )
        
        self.assertIn('login', driver.current_url)
        print("✓ Потребителят успешно излезе от системата")


if __name__ == '__main__':
    unittest.main(verbosity=2)
