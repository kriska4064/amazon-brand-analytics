-- =============================================================================
-- MIGRATION 002: ADD PERFORMANCE INDEXES
-- =============================================================================
-- Автор: Христо Мишев
-- Дата: 10 Ноември 2025
-- Цел: Добавяне на индекси за подобряване на производителността
-- =============================================================================

USE amazon_brand_analytics;

-- Допълнителни composite indexes за често използвани заявки

-- Products таблица
ALTER TABLE products 
ADD INDEX idx_brand_category (brand, category);

ALTER TABLE products 
ADD INDEX idx_rating_reviews (rating, reviews_count);

-- Price history таблица
ALTER TABLE price_history 
ADD INDEX idx_price_recorded (price, recorded_at);

-- Search keywords таблица
ALTER TABLE search_keywords 
ADD INDEX idx_volume_keyword (search_volume DESC, keyword);

-- System logs таблица
ALTER TABLE system_logs 
ADD INDEX idx_action_created (action, created_at);

-- Записване на миграцията
INSERT INTO schema_migrations (version, description) 
VALUES ('002', 'Added composite indexes for query optimization');

-- =============================================================================
-- КРАЙ НА MIGRATION 002
-- =============================================================================
