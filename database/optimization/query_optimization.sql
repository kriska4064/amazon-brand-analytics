-- =============================================================================
-- QUERY OPTIMIZATION - Оптимизирани заявки
-- =============================================================================
-- Автор: Христо Мишев
-- Дата: 25 Ноември 2025
-- Цел: Колекция от оптимизирани заявки за често използвани операции
-- =============================================================================

USE amazon_brand_analytics;

-- =============================================================================
-- 1. ТОП 10 ПРОДУКТА ПО РЕЙТИНГ
-- =============================================================================
-- Оптимизирана версия с използване на индекси
SELECT 
    product_id,
    asin,
    title,
    brand,
    rating,
    reviews_count,
    price
FROM products 
WHERE rating IS NOT NULL 
  AND reviews_count >= 10
ORDER BY rating DESC, reviews_count DESC 
LIMIT 10;

-- =============================================================================
-- 2. АНАЛИЗ НА ЦЕНОВИ ПРОМЕНИ ЗА ПОСЛЕДНИТЕ 30 ДНИ
-- =============================================================================
SELECT 
    p.asin,
    p.title,
    p.brand,
    MIN(ph.price) AS min_price,
    MAX(ph.price) AS max_price,
    AVG(ph.price) AS avg_price,
    COUNT(ph.price_history_id) AS price_changes
FROM products p
INNER JOIN price_history ph ON p.product_id = ph.product_id
WHERE ph.recorded_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY p.product_id, p.asin, p.title, p.brand
HAVING price_changes > 1
ORDER BY price_changes DESC
LIMIT 20;

-- =============================================================================
-- 3. ТОП КЛЮЧОВИ ДУМИ ПО ОБЕМ НА ТЪРСЕНЕ
-- =============================================================================
SELECT 
    sk.keyword,
    sk.search_volume,
    COUNT(DISTINCT pk.product_id) AS associated_products,
    AVG(pk.relevance_score) AS avg_relevance
FROM search_keywords sk
LEFT JOIN product_keywords pk ON sk.keyword_id = pk.keyword_id
GROUP BY sk.keyword_id, sk.keyword, sk.search_volume
ORDER BY sk.search_volume DESC
LIMIT 15;

-- =============================================================================
-- 4. АНАЛИЗ НА КОНКУРЕНТИ ПО МАРКИ
-- =============================================================================
SELECT 
    p.brand,
    COUNT(DISTINCT p.product_id) AS total_products,
    AVG(p.rating) AS avg_rating,
    AVG(p.price) AS avg_price,
    SUM(p.reviews_count) AS total_reviews,
    c.market_share
FROM products p
LEFT JOIN competitors c ON p.brand = c.brand
GROUP BY p.brand, c.market_share
ORDER BY total_products DESC, avg_rating DESC
LIMIT 10;

-- =============================================================================
-- 5. ПРОДУКТИ С НАЙ-МНОГО ПРОМЕНИ В ЦЕНИТЕ (VOLATILITY)
-- =============================================================================
SELECT 
    p.asin,
    p.title,
    p.brand,
    COUNT(ph.price_history_id) AS price_changes,
    STDDEV(ph.price) AS price_volatility,
    MIN(ph.price) AS min_price,
    MAX(ph.price) AS max_price
FROM products p
INNER JOIN price_history ph ON p.product_id = ph.product_id
WHERE ph.recorded_at >= DATE_SUB(NOW(), INTERVAL 90 DAY)
GROUP BY p.product_id, p.asin, p.title, p.brand
HAVING price_changes >= 5
ORDER BY price_volatility DESC
LIMIT 15;

-- =============================================================================
-- 6. СТАТИСТИКА ЗА АКТИВНОСТ НА ПОТРЕБИТЕЛИ
-- =============================================================================
SELECT 
    u.username,
    u.full_name,
    u.role,
    COUNT(DISTINCT r.report_id) AS total_reports,
    MAX(u.last_login) AS last_active
FROM users u
LEFT JOIN reports r ON u.user_id = r.user_id
WHERE u.is_active = TRUE
GROUP BY u.user_id, u.username, u.full_name, u.role
ORDER BY total_reports DESC;

-- =============================================================================
-- 7. ИЗЧИСТВАНЕ НА ИЗТЕКЛИ КЕШИРАНИ ДАННИ
-- =============================================================================
DELETE FROM cache_data 
WHERE expires_at < NOW();

-- =============================================================================
-- КРАЙ НА QUERY OPTIMIZATION
-- =============================================================================
