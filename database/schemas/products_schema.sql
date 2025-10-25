-- =============================================================================
-- PRODUCTS SCHEMA - Amazon Brand Analytics Database
-- =============================================================================
-- Автор: Христо Мишев
-- Дата: 25 Октомври 2025
-- Цел: Основна схема за продуктови данни от Amazon API
-- =============================================================================

CREATE DATABASE IF NOT EXISTS amazon_brand_analytics 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE amazon_brand_analytics;

-- Таблица за продукти
CREATE TABLE IF NOT EXISTS products (
    product_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    asin VARCHAR(10) UNIQUE NOT NULL COMMENT 'Amazon Standard Identification Number',
    title VARCHAR(500) NOT NULL COMMENT 'Заглавие на продукта',
    brand VARCHAR(200) NOT NULL COMMENT 'Марка на продукта',
    category VARCHAR(200) DEFAULT NULL COMMENT 'Категория',
    price DECIMAL(10,2) DEFAULT NULL COMMENT 'Текуща цена в лева',
    currency CHAR(3) DEFAULT 'BGN' COMMENT 'Валута',
    rating DECIMAL(3,2) DEFAULT NULL COMMENT 'Среден рейтинг (0-5)',
    reviews_count INT UNSIGNED DEFAULT 0 COMMENT 'Брой ревюта',
    image_url VARCHAR(500) DEFAULT NULL COMMENT 'URL на основна снимка',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Последна актуализация',
    INDEX idx_brand (brand),
    INDEX idx_category (category),
    INDEX idx_price (price),
    INDEX idx_rating (rating),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Основна таблица за продукти от Amazon';

-- Таблица за исторически данни за цени
CREATE TABLE IF NOT EXISTS price_history (
    price_history_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT UNSIGNED NOT NULL COMMENT 'Връзка към продукта',
    price DECIMAL(10,2) NOT NULL COMMENT 'Цена към момента',
    currency CHAR(3) DEFAULT 'BGN',
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на записване',
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    INDEX idx_product_recorded (product_id, recorded_at),
    INDEX idx_price (price)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='История на промени в цените';

-- Таблица за ключови думи и търсения
CREATE TABLE IF NOT EXISTS search_keywords (
    keyword_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(200) NOT NULL UNIQUE COMMENT 'Ключова дума',
    search_volume INT UNSIGNED DEFAULT 0 COMMENT 'Обем на търсене',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_keyword (keyword),
    INDEX idx_search_volume (search_volume)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Ключови думи за търсене';

-- Връзка продукти-ключови думи (many-to-many)
CREATE TABLE IF NOT EXISTS product_keywords (
    product_id BIGINT UNSIGNED NOT NULL,
    keyword_id BIGINT UNSIGNED NOT NULL,
    relevance_score DECIMAL(5,2) DEFAULT 0.00 COMMENT 'Релевантност (0-100)',
    PRIMARY KEY (product_id, keyword_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES search_keywords(keyword_id) ON DELETE CASCADE,
    INDEX idx_relevance (relevance_score)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Връзка между продукти и ключови думи';

-- Таблица за конкуренти
CREATE TABLE IF NOT EXISTS competitors (
    competitor_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    brand VARCHAR(200) NOT NULL UNIQUE COMMENT 'Име на конкурентна марка',
    market_share DECIMAL(5,2) DEFAULT NULL COMMENT 'Пазарен дял (%)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_brand (brand)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Конкурентни марки';

-- =============================================================================
-- КРАЙ НА СХЕМА
-- =============================================================================
