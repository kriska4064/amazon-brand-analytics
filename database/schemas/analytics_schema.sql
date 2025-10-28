-- =============================================================================
-- ANALYTICS SCHEMA - Допълнителни аналитични таблици
-- =============================================================================
-- Автор: Христо Мишев
-- Дата: 30 Октомври 2025
-- Цел: Схема за анализи и отчети
-- =============================================================================

USE amazon_brand_analytics;

-- Таблица за потребители на системата
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL COMMENT 'Потребителско име',
    email VARCHAR(150) UNIQUE NOT NULL COMMENT 'Имейл адрес',
    password_hash VARCHAR(255) NOT NULL COMMENT 'Hash на паролата',
    full_name VARCHAR(200) DEFAULT NULL COMMENT 'Пълно име',
    role ENUM('admin', 'analyst', 'viewer') DEFAULT 'viewer' COMMENT 'Роля в системата',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Активен акаунт',
    last_login TIMESTAMP NULL DEFAULT NULL COMMENT 'Последно влизане',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_role (role)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Потребители на аналитичната система';

-- Таблица за логове на системата
CREATE TABLE IF NOT EXISTS system_logs (
    log_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED DEFAULT NULL COMMENT 'Потребител, ако е приложимо',
    action VARCHAR(100) NOT NULL COMMENT 'Извършено действие',
    entity VARCHAR(100) DEFAULT NULL COMMENT 'Обект на действието',
    entity_id BIGINT UNSIGNED DEFAULT NULL COMMENT 'ID на обекта',
    ip_address VARCHAR(45) DEFAULT NULL COMMENT 'IP адрес',
    user_agent TEXT DEFAULT NULL COMMENT 'User agent string',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_user_action (user_id, action),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Логове на системни действия';

-- Таблица за генерирани отчети
CREATE TABLE IF NOT EXISTS reports (
    report_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL COMMENT 'Потребител, създал отчета',
    report_type ENUM('sales', 'pricing', 'keywords', 'competitors') NOT NULL COMMENT 'Тип на отчета',
    title VARCHAR(200) NOT NULL COMMENT 'Заглавие на отчета',
    description TEXT DEFAULT NULL COMMENT 'Описание',
    parameters JSON DEFAULT NULL COMMENT 'Параметри на отчета',
    file_path VARCHAR(500) DEFAULT NULL COMMENT 'Път до генериран файл',
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending' COMMENT 'Статус',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_type (user_id, report_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Генерирани аналитични отчети';

-- Таблица за кеширани данни (за оптимизация)
CREATE TABLE IF NOT EXISTS cache_data (
    cache_key VARCHAR(255) PRIMARY KEY COMMENT 'Уникален ключ за кеша',
    cache_value LONGTEXT NOT NULL COMMENT 'Стойност (JSON или текст)',
    expires_at TIMESTAMP NOT NULL COMMENT 'Дата на изтичане',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_expires (expires_at)
) ENGINE=InnoDB 
  DEFAULT CHARSET=utf8mb4 
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Кеш данни за оптимизация';

-- =============================================================================
-- КРАЙ НА ANALYTICS SCHEMA
-- =============================================================================
