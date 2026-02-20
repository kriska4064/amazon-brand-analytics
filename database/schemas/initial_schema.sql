-- Схема на База Данни за Софтуер за Анализ на Брандове в Amazon
-- Автор: Христо Мишев (дизайн от Мартин Дачев)
-- Дата: 2025-06-20
-- Проект: ЕС BG16RFPR001-1.001

CREATE DATABASE IF NOT EXISTS amazon_analytics 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE amazon_analytics;

-- Таблица Брандове
CREATE TABLE IF NOT EXISTS brands (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL COMMENT 'Име на бранда',
    seller_name VARCHAR(255) COMMENT 'Име на продавача',
    category VARCHAR(100) COMMENT 'Категория',
    amazon_store_url VARCHAR(500) COMMENT 'URL на Amazon магазин',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Дата на обновяване',
    INDEX idx_brand_name (brand_name),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица с брандове';

-- Таблица Продукти
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_id INT NOT NULL COMMENT 'ID на бранда',
    asin VARCHAR(10) NOT NULL UNIQUE COMMENT 'Amazon ASIN код',
    title VARCHAR(500) COMMENT 'Заглавие на продукта',
    price DECIMAL(10, 2) COMMENT 'Цена',
    currency VARCHAR(3) DEFAULT 'EUR' COMMENT 'Валута',
    rating DECIMAL(3, 2) COMMENT 'Рейтинг',
    reviews_count INT DEFAULT 0 COMMENT 'Брой отзиви',
    image_url VARCHAR(500) COMMENT 'URL на изображение',
    product_url VARCHAR(500) COMMENT 'URL на продукта',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Дата на обновяване',
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE,
    INDEX idx_asin (asin),
    INDEX idx_brand_id (brand_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица с продукти';

-- Таблица Ключови Думи
CREATE TABLE IF NOT EXISTS keywords (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    keyword_text VARCHAR(255) NOT NULL COMMENT 'Текст на ключова дума',
    search_volume INT DEFAULT 0 COMMENT 'Обем на търсене',
    competition_level VARCHAR(20) COMMENT 'Ниво на конкуренция',
    category VARCHAR(100) COMMENT 'Категория',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Дата на обновяване',
    UNIQUE KEY unique_keyword (keyword_text),
    INDEX idx_keyword_text (keyword_text),
    INDEX idx_search_volume (search_volume)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица с ключови думи';

-- Таблица Класирания
CREATE TABLE IF NOT EXISTS rankings (
    ranking_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL COMMENT 'ID на продукта',
    keyword_id INT NOT NULL COMMENT 'ID на ключова дума',
    position INT COMMENT 'Позиция в резултатите',
    page_number INT COMMENT 'Номер на страница',
    is_sponsored BOOLEAN DEFAULT FALSE COMMENT 'Дали е спонсорирана',
    ranking_date DATE NOT NULL COMMENT 'Дата на класирането',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id) ON DELETE CASCADE,
    INDEX idx_product_keyword (product_id, keyword_id),
    INDEX idx_ranking_date (ranking_date),
    INDEX idx_position (position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица с класирания';

-- Таблица Конкуренти
CREATE TABLE IF NOT EXISTS competitors (
    competitor_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_id INT NOT NULL COMMENT 'ID на бранда',
    competitor_brand_name VARCHAR(255) NOT NULL COMMENT 'Име на бранд конкурент',
    competitor_asin VARCHAR(10) COMMENT 'ASIN на конкурент',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE,
    INDEX idx_brand_id (brand_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица с конкуренти';

-- Таблица Аналитични Снимки
CREATE TABLE IF NOT EXISTS analytics_snapshots (
    snapshot_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_id INT NOT NULL COMMENT 'ID на бранда',
    snapshot_date DATE NOT NULL COMMENT 'Дата на снимката',
    average_position DECIMAL(5, 2) COMMENT 'Средна позиция',
    visibility_score DECIMAL(5, 2) COMMENT 'Показател за видимост',
    total_keywords INT DEFAULT 0 COMMENT 'Общо ключови думи',
    top_10_keywords INT DEFAULT 0 COMMENT 'Ключови думи в топ 10',
    data_json TEXT COMMENT 'JSON данни',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE,
    INDEX idx_brand_date (brand_id, snapshot_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица с аналитични снимки';

-- Таблица Потребители
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE COMMENT 'Имейл',
    username VARCHAR(100) NOT NULL UNIQUE COMMENT 'Потребителско име',
    password_hash VARCHAR(255) NOT NULL COMMENT 'Хеш на парола',
    role VARCHAR(50) DEFAULT 'user' COMMENT 'Роля',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    last_login TIMESTAMP NULL COMMENT 'Последно влизане',
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица с потребители';

-- Таблица API Логове
CREATE TABLE IF NOT EXISTS api_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    endpoint VARCHAR(255) COMMENT 'API endpoint',
    method VARCHAR(10) COMMENT 'HTTP метод',
    status_code INT COMMENT 'Код на статус',
    response_time_ms INT COMMENT 'Време за отговор в ms',
    error_message TEXT COMMENT 'Съобщение за грешка',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата на създаване',
    INDEX idx_created_at (created_at),
    INDEX idx_endpoint (endpoint)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Таблица с API логове';
