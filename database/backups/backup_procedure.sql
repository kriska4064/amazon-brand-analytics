-- =============================================================================
-- BACKUP PROCEDURES - Процедури за резервно копие
-- =============================================================================
-- Автор: Христо Мишев
-- Дата: 15 Януари 2026
-- Цел: Автоматизирани процедури за backup и възстановяване
-- =============================================================================

USE amazon_brand_analytics;

DELIMITER //

-- =============================================================================
-- ПРОЦЕДУРА: Създаване на backup на таблица
-- =============================================================================
CREATE PROCEDURE IF NOT EXISTS backup_table(
    IN table_name VARCHAR(100)
)
BEGIN
    DECLARE backup_table_name VARCHAR(150);
    DECLARE backup_timestamp VARCHAR(20);
    
    -- Генериране на име с timestamp
    SET backup_timestamp = DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s');
    SET backup_table_name = CONCAT(table_name, '_backup_', backup_timestamp);
    
    -- Създаване на backup таблица
    SET @sql = CONCAT('CREATE TABLE ', backup_table_name, ' AS SELECT * FROM ', table_name);
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SELECT CONCAT('Backup created: ', backup_table_name) AS message;
END//

-- =============================================================================
-- ПРОЦЕДУРА: Изтриване на стари backup таблици
-- =============================================================================
CREATE PROCEDURE IF NOT EXISTS cleanup_old_backups(
    IN days_to_keep INT
)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE tbl_name VARCHAR(150);
    DECLARE cur CURSOR FOR 
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'amazon_brand_analytics' 
          AND table_name LIKE '%_backup_%'
          AND create_time < DATE_SUB(NOW(), INTERVAL days_to_keep DAY);
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO tbl_name;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        SET @sql = CONCAT('DROP TABLE IF EXISTS ', tbl_name);
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
        SELECT CONCAT('Deleted old backup: ', tbl_name) AS message;
    END LOOP;
    
    CLOSE cur;
END//

-- =============================================================================
-- ПРОЦЕДУРА: Статистика за размери на таблици
-- =============================================================================
CREATE PROCEDURE IF NOT EXISTS table_size_stats()
BEGIN
    SELECT 
        table_name AS 'Таблица',
        ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Размер (MB)',
        table_rows AS 'Брой редове',
        ROUND((data_length / 1024 / 1024), 2) AS 'Данни (MB)',
        ROUND((index_length / 1024 / 1024), 2) AS 'Индекси (MB)'
    FROM information_schema.tables
    WHERE table_schema = 'amazon_brand_analytics'
    ORDER BY (data_length + index_length) DESC;
END//

DELIMITER ;

-- =============================================================================
-- ПРИМЕРНО ИЗВИКВАНЕ:
-- CALL backup_table('products');
-- CALL cleanup_old_backups(30);
-- CALL table_size_stats();
-- =============================================================================

-- =============================================================================
-- КРАЙ НА BACKUP PROCEDURES
-- =============================================================================
