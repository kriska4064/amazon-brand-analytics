# 📊 Аналитична документация - Amazon Brand Analytics

**Анализатор на данни:** Диана Георгиева  
**Роля:** Data Analyst / BI Специалист (8 часа/ден)  
**Период:** 21 Юни 2025 – 19 Февруари 2026  
**Проект:** Amazon Brand Analytics (SP LINK)  
**TRL прогрес:** TRL 3 → TRL 5

---

## 📋 Обобщение

Тази документация описва аналитичните инструменти и процеси, разработени за проекта Amazon Brand Analytics.

---

## 🎯 Основни компоненти

### 1️⃣ Data Collection (`analytics/data_collection.py`)

**Цел:** Събиране на данни от Amazon API

**Функционалности:**
- Събиране на продуктови данни по категория
- Извличане на ценова история
- Събиране на конкурентни данни
- Експорт към CSV/DataFrame

**Използване:**
```python
from analytics.data_collection import AmazonDataCollector

collector = AmazonDataCollector(api_key='...', base_url='...')
products = collector.collect_products(category='Electronics', limit=100)
collector.save_to_csv(products, 'products.csv')
```

---

### 2️⃣ ETL Pipeline (`data-pipelines/etl_pipeline.py`)

**Цел:** Extract, Transform, Load процес за почистване на данни

**Етапи:**
1. **Extract** - Извличане от CSV
2. **Transform** - Почистване, валидация, изчислени колони
3. **Load** - Запазване на обработени данни

**Трансформации:**
- Премахване на дубликати
- Попълване на липсващи стойности
- Валидация на цени и рейтинги
- Изчисляване на popularity score
- Категоризиране на цени и рейтинги

**Използване:**
```python
from data_pipelines.etl_pipeline import AmazonETLPipeline

pipeline = AmazonETLPipeline()
pipeline.run_pipeline(source_path='raw.csv', output_path='clean.csv')
```

---

### 3️⃣ Competitor Analysis (`analytics/competitor_analysis.py`)

**Цел:** Анализ на конкурентни марки и пазарен дял

**Анализи:**
- Пазарен дял по марки
- Ценово позициониране (Premium, Mid-range, Budget)
- Качество vs Цена анализ
- Competitive Advantage Score

**Метрики:**
- Market share percentage
- Average price per brand
- Average rating
- Total reviews
- Competitive advantage score (weighted)

**Използване:**
```python
from analytics.competitor_analysis import CompetitorAnalyzer

analyzer = CompetitorAnalyzer(data)
brand_stats = analyzer.analyze_by_brand()
top10 = analyzer.get_top_competitors(10)
analyzer.generate_competitor_report()
```

---

### 4️⃣ Sales Dashboard (`dashboards/sales_dashboard.py`)

**Цел:** Интерактивен dashboard с Plotly

**Визуализации:**
- Bar chart - Топ марки по пазарен дял
- Box plot - Разпределение на цени по категория
- Scatter plot - Цена vs Рейтинг
- Pie chart - Ценови категории

**KPI Метрики:**
- Общо продукти
- Брой марки
- Средна цена
- Среден рейтинг
- Общо ревюта

**Използване:**
```python
from dashboards.sales_dashboard import SalesDashboard

dashboard = SalesDashboard(data)
dashboard.create_dashboard()
dashboard.save_dashboard('dashboard.html')
```

---

## 📊 Ключови метрики

### Popularity Score

**Formula:**
```
Popularity Score = (rating × 20) + (log10(reviews_count + 1) × 10)
```

**Диапазон:** 0-150
- 0-40: Ниска популярност
- 40-80: Средна популярност
- 80-120: Висока популярност
- 120+: Много висока популярност

---

### Competitive Advantage Score

**Formula (weighted average):**
```
CA Score = (Rating Score × 0.30) +
           (Market Share Score × 0.25) +
           (Review Volume Score × 0.25) +
           (Price Competitiveness × 0.20)
```

**Диапазон:** 0-100

---

## 📈 Workflow

```
1. Data Collection
   └─> Събиране от Amazon API
       └─> Запазване в CSV

2. ETL Pipeline
   └─> Extract от CSV
       └─> Transform (cleaning, validation)
           └─> Load обработени данни

3. Analytics
   └─> Competitor Analysis
   └─> Sales Dashboard
   └─> Predictive Models

4. Reporting
   └─> Automated Reports
   └─> Business Insights
```

---

## 🛠️ Технологии

- **Python 3.9+**
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **plotly** - Interactive visualizations
- **matplotlib / seaborn** - Static plots
- **requests** - API calls
- **scikit-learn** - Machine learning (predictive models)

---

## 📦 Зависимости

```
pandas>=1.3.0
numpy>=1.21.0
plotly>=5.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
requests>=2.26.0
scikit-learn>=1.0.0
```

---

## 🚀 Бързо начало

### 1. Инсталиране на зависимости

```bash
pip install -r requirements.txt
```

### 2. Събиране на данни

```python
from analytics.data_collection import AmazonDataCollector

collector = AmazonDataCollector(api_key='YOUR_API_KEY', base_url='API_URL')
products = collector.collect_products(category='Electronics', limit=1000)
collector.save_to_csv(products, 'amazon_products_raw.csv')
```

### 3. Обработка на данни (ETL)

```python
from data_pipelines.etl_pipeline import AmazonETLPipeline

pipeline = AmazonETLPipeline()
pipeline.run_pipeline(
    source_path='amazon_products_raw.csv',
    output_path='amazon_products_clean.csv'
)
```

### 4. Анализ и визуализация

```python
import pandas as pd
from analytics.competitor_analysis import CompetitorAnalyzer
from dashboards.sales_dashboard import SalesDashboard

# Зареждане на данни
data = pd.read_csv('amazon_products_clean.csv')

# Конкурентен анализ
analyzer = CompetitorAnalyzer(data)
analyzer.analyze_by_brand()
analyzer.generate_competitor_report()

# Dashboard
dashboard = SalesDashboard(data)
dashboard.create_dashboard()
dashboard.save_dashboard('sales_dashboard.html')
```

---

## 📞 Контакт

**Име:** Диана Георгиева  
**Роля:** Data Analyst / BI Специалист  
**Email:** diana.georgieva@example.com  
**GitHub:** @dianaGeorgieva

---

**Последна актуализация:** 15 Февруари 2026  
**Версия:** 1.0  
**TRL Ниво:** TRL 5 ✅
