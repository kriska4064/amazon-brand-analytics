-- =============================================================================
-- MIGRATION 001: INITIAL DATABASE SETUP
-- =============================================================================
-- Автор: Христо Мишев
-- Дата: 25 Октомври 2025
-- Цел: Първоначално създаване на база данни и основни таблици
-- =============================================================================

-- Създаване на база данни
CREATE DATABASE IF NOT EXISTS amazon_brand_analytics 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE amazon_brand_analytics;

-- Основни таблици създадени в products_schema.sql
-- Този migration файл удостоверява версията и статуса

CREATE TABLE IF NOT EXISTS schema_migrations (
    migration_id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    version VARCHAR(50) UNIQUE NOT NULL COMMENT 'Версия на миграцията',
    description VARCHAR(255) DEFAULT NULL COMMENT 'Описание',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на прилагане',
    INDEX idx_version (version)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='История на миграциите';

-- Записване на текущата миграция
INSERT INTO schema_migrations (version, description) 
VALUES ('001', 'Initial database setup with products and analytics schemas');

-- =============================================================================
-- КРАЙ НА MIGRATION 001
-- =============================================================================
