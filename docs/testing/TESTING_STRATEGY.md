# 🧪 Тестова стратегия - Amazon Brand Analytics

**Тестов инженер:** Цвета Попова  
**Роля:** QA/Testing Engineer (4 часа/ден)  
**Период:** 20 Октомври 2025 – 19 Февруари 2026  
**Проект:** Amazon Brand Analytics (SP LINK)

---

## 📋 Обща информация

Тази документация описва цялостната тестова стратегия за проекта Amazon Brand Analytics, покриваща периода от **TRL 4** до **TRL 5**.

---

## 🎯 Цели на тестването

1. **Осигуряване на качество** - Гарантиране че софтуерът работи коректно
2. **Валидация на функционалности** - Всички features работят според изискванията
3. **Performance testing** - Системата отговаря в рамките на целевите времена
4. **User acceptance** - Потребителите са доволни от платформата
5. **TRL 5 validation** - Готовност за production deployment

---

## 🧪 Видове тестове

### 1️⃣ Unit Testing (Юнит тестове)

**Описание:** Тестване на отделни модули/функции изолирано.

**Фреймуърк:** `unittest` (Python) / `Jest` (JavaScript)

**Покритие:** Цел 80%+

**Модули:**
- Products
- Price History
- Keywords
- Users
- Competitors

**Пример:**
```python
def test_product_creation(self):
    product = Product(asin='B08N5WRWNW', title='Echo Dot')
    self.assertEqual(product.asin, 'B08N5WRWNW')
```

---

### 2️⃣ Integration Testing (Интеграционни тестове)

**Описание:** Тестване на взаимодействието между различни модули.

**Инструменти:** `requests` (Python), `Postman`

**API Endpoints тествани:**
- `/products` (GET, POST, PUT, DELETE)
- `/price-history` (GET, POST)
- `/keywords` (GET, POST)
- `/users` (GET, POST, PUT, DELETE)

**Пример:**
```python
response = requests.get(f'{base_url}/products/{asin}')
self.assertEqual(response.status_code, 200)
```

---

### 3️⃣ End-to-End Testing (E2E тестове)

**Описание:** Тестване на цялостни потребителски сценарии.

**Инструменти:** `Selenium WebDriver`, `Cypress`

**Сценарии:**
- User login → Search products → View details → Logout
- Add product to watchlist → Receive notification
- Generate report → Export to PDF

**Пример:**
```python
driver.get('http://localhost:3000/login')
username_field = driver.find_element(By.ID, 'username')
username_field.send_keys('test_user')
```

---

### 4️⃣ Performance Testing

**Описание:** Измерване на скоростта и производителността.

**Инструменти:** `Apache JMeter`, `Locust`

**Метрики:**
- Response time (средно време за отговор)
- Throughput (заявки в секунда)
- Error rate (процент грешки)

**Целеви времена:**
| Endpoint | Цел |
|----------|-----|
| GET /products | <100ms |
| POST /products | <150ms |
| GET /price-history | <200ms |

---

### 5️⃣ User Acceptance Testing (UAT)

**Описание:** Тестване с реални потребители (pilot testing).

**Период:** Януари 2026

**Брой потребители:** 5

**Метрики:**
- System Usability Scale (SUS)
- User satisfaction (1-5 звезди)
- Task completion rate

---

## 📅 Тестов график

### **Октомври 2025 (TRL 4)**
- Setup на testing framework
- Unit тестове за основни модули
- Инициализация на test environment

### **Ноември 2025 (TRL 4)**
- Integration тестове за API endpoints
- Performance baseline измервания
- Bug tracking setup

### **Декември 2025 (TRL 4→5)**
- E2E тестове (Selenium)
- Test automation setup
- Regression testing

### **Януари 2026 (TRL 5)**
- Pilot testing с реални потребители
- UAT (User Acceptance Testing)
- Bug fixing и re-testing

### **Февруари 2026 (TRL 5)**
- Final testing преди одит
- Performance optimization validation
- Production readiness check

---

## 🐛 Bug Tracking

**Инструмент:** GitHub Issues

**Приоритети:**
- 🔴 **Critical** - Блокира основна функционалност
- 🟡 **High** - Сериозен проблем, не блокира
- 🟢 **Medium** - Малък проблем
- ⚪ **Low** - Козметичен проблем

**Bug lifecycle:**
1. **Open** - Бъгът е открит
2. **Assigned** - Assign-нат на разработчик
3. **In Progress** - Работи се по fix-а
4. **Fixed** - Поправен, чака re-test
5. **Verified** - Потвърден като fix-нат
6. **Closed** - Затворен

---

## 📊 Test Coverage

**Цел:** 80%+ code coverage

**Актуално покритие (Ноември 2025):**
- Backend (Python): 79%
- Frontend (JavaScript): 75%
- Database queries: 85%

**Инструменти:**
- `coverage.py` (Python)
- `Jest --coverage` (JavaScript)

---

## ✅ Критерии за успех

### TRL 4 изисквания:
- ✅ Всички unit тестове преминават (100%)
- ✅ Integration тестове покриват всички API endpoints
- ✅ Bug rate <5%

### TRL 5 изисквания:
- ✅ E2E тестове за всички критични сценарии
- ✅ Pilot testing с минимум 5 реални потребители
- ✅ SUS скор >68 (над средното)
- ✅ User satisfaction >4/5
- ✅ Няма critical bugs

---

## 🚀 CI/CD Integration

**Pipeline:**
1. **Commit** → Автоматични unit тестове
2. **Pull Request** → Regression тестове
3. **Merge to main** → Full test suite
4. **Deploy to staging** → Smoke тестове
5. **Deploy to production** → Monitoring

**Инструменти:**
- GitHub Actions
- Jenkins (опционално)

---

## 📞 Контакт

При въпроси или проблеми свързани с тестването:

**Име:** Цвета Попова  
**Роля:** QA/Testing Engineer  
**Email:** tsveta.popova@example.com  
**GitHub:** @tsvetaPopova

---

**Последна актуализация:** 15 Февруари 2026  
**Версия:** 1.3
