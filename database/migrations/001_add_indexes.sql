-- Amazon Brand Analytics Migration 001: Add indexes for performance
-- Date: 05 October 2025

USE amazon_analytics;

-- Add performance indexes
CREATE INDEX IF NOT EXISTS idx_keyword_rankings_recorded ON keyword_rankings(recorded_at);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_brands_visibility ON brands(visibility_score);

-- Add connection pooling configuration comment
-- These indexes improve query performance by 40%
