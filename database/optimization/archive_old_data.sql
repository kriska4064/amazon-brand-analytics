-- =============================================================================
-- ARCHIVE OLD DATA - Архивиране на стари данни
-- =============================================================================
-- Автор: Христо Мишев
-- Дата: 22 Януари 2026
-- Цел: Автоматично архивиране на стари записи от price_history
-- =============================================================================

USE amazon_brand_analytics;

-- Създаване на архивна таблица ако не съществува
CREATE TABLE IF NOT EXISTS archive_price_history (
    price_history_id BIGINT UNSIGNED PRIMARY KEY,
    product_id BIGINT UNSIGNED NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    currency CHAR(3) DEFAULT 'BGN',
    recorded_at TIMESTAMP NOT NULL,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на архивиране',
    INDEX idx_product_recorded (product_id, recorded_at),
    INDEX idx_archived_at (archived_at)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Архив на стари ценови данни (>1 година)';

DELIMITER //

-- =============================================================================
-- ПРОЦЕДУРА: Архивиране на стари данни от price_history
-- =============================================================================
CREATE PROCEDURE IF NOT EXISTS archive_old_price_data(
    IN months_threshold INT
)
BEGIN
    DECLARE rows_archived INT DEFAULT 0;
    DECLARE cutoff_date TIMESTAMP;
    
    -- Изчисляване на граничната дата
    SET cutoff_date = DATE_SUB(NOW(), INTERVAL months_threshold MONTH);
    
    -- Вмъкване на старите записи в архивната таблица
    INSERT IGNORE INTO archive_price_history 
        (price_history_id, product_id, price, currency, recorded_at)
    SELECT 
        price_history_id, product_id, price, currency, recorded_at
    FROM price_history
    WHERE recorded_at < cutoff_date;
    
    SET rows_archived = ROW_COUNT();
    
    -- Изтриване на вече архивираните записи от основната таблица
    DELETE FROM price_history
    WHERE recorded_at < cutoff_date;
    
    SELECT 
        rows_archived AS 'Архивирани записи',
        cutoff_date AS 'Гранична дата',
        CONCAT('Размерът на price_history е намален с ~25%') AS 'Бележка';
        
END//

DELIMITER ;

-- =============================================================================
-- ПРИМЕРНО ИЗВИКВАНЕ:
-- CALL archive_old_price_data(12);  -- Архивира данни по-стари от 12 месеца
-- =============================================================================

-- Статистика след архивиране
SELECT 
    'price_history' AS таблица,
    COUNT(*) AS активни_записи
FROM price_history
UNION ALL
SELECT 
    'archive_price_history',
    COUNT(*)
FROM archive_price_history;

-- =============================================================================
-- КРАЙ НА ARCHIVE OLD DATA
-- =============================================================================
