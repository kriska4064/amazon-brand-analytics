-- Amazon Brand Analytics - Initial Database Schema
-- Version: 1.0.0
-- Created: 15 June 2025

CREATE DATABASE IF NOT EXISTS amazon_analytics 
  CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

USE amazon_analytics;

-- Brands table
CREATE TABLE IF NOT EXISTS brands (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    amazon_store_id VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100),
    visibility_score DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_amazon_store_id (amazon_store_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    asin VARCHAR(20) UNIQUE NOT NULL,
    brand_id INT,
    title VARCHAR(500) NOT NULL,
    price DECIMAL(10,2),
    rating DECIMAL(3,2),
    review_count INT DEFAULT 0,
    category VARCHAR(100),
    rank INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE,
    INDEX idx_asin (asin),
    INDEX idx_brand_id (brand_id),
    INDEX idx_rank (rank)
) ENGINE=InnoDB;

-- Keywords table
CREATE TABLE IF NOT EXISTS keywords (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    search_volume INT DEFAULT 0,
    competition_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_keyword (keyword),
    INDEX idx_keyword (keyword)
) ENGINE=InnoDB;

-- Keyword rankings table (tracks position over time)
CREATE TABLE IF NOT EXISTS keyword_rankings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    keyword_id INT NOT NULL,
    position INT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(id) ON DELETE CASCADE,
    INDEX idx_product_keyword (product_id, keyword_id),
    INDEX idx_recorded_at (recorded_at)
) ENGINE=InnoDB;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    amazon_seller_id VARCHAR(100),
    role ENUM('admin', 'user', 'pilot_tester') DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB;

-- User feedback table (for pilot testing)
CREATE TABLE IF NOT EXISTS user_feedback (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    rating TINYINT CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    feature VARCHAR(100),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_submitted_at (submitted_at)
) ENGINE=InnoDB;

-- Analytics events table
CREATE TABLE IF NOT EXISTS analytics_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(36),
    event_type VARCHAR(100) NOT NULL,
    event_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_event_type (event_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB;
