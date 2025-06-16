# Amazon Brand Analytics - Проектен план
## Проект BG16RFPR001-1.001

**Създаден от:** Мария Далева  
**Дата:** 18 Юни 2025  
**Версия:** 1.0

---

## 1. ПРОЕКТНА ИНФОРМАЦИЯ

### Основни данни
- **Име на проект:** Разработка на софтуерен прототип за анализ на брандове в Amazon платформата
- **Код на проект:** BG16RFPR001-1.001
- **Програма:** ISUN 2020 - Иновации и конкурентоспособност
- **Бенефициент:** SP LINK ЕООД (преди НЕКСО)
- **Адрес:** Пазарджик, ул. Цар Шишман №28

### Финансова информация
- **Обща стойност:** 297,600 BGN
- **Продължителност:** 18 месеца
- **Начало:** Юни 2025
- **Край:** Декември 2026

---

## 2. ЦЕЛИ НА ПРОЕКТА

### Главна цел
Разработка на функционален софтуерен прототип за анализ и оптимизация на брандове продавани в Amazon платформата, достигащ технологична готовност TRL 7.

### Специфични цели
1. Интеграция с Amazon Product Advertising API и Selling Partner API
2. Автоматизирано събиране и обработка на данни за продукти
3. Анализ на keyword rankings и visibility
4. Competitor analysis и benchmarking
5. Visualization dashboard за brand performance
6. Export и reporting функционалности

---

## 3. TEAM СТРУКТУРА

### Екип (6 души)

#### Martin Dachev - Програмист, софтуерни приложения
- **Часове:** 4 часа/ден
- **Email:** martin.da4ev@gmail.com
- **Роля:** Lead Developer, Backend Architecture
- **Отговорности:** 
  - Backend development (Python, Flask)
  - Amazon API integration
  - Database design
  - Performance optimization

#### Kristina Todorova - Програмист, софтуерни приложения
- **Часове:** 8 часа/ден (пълен работен ден)
- **Email:** kriska_4064@icloud.com
- **Роля:** Frontend Developer
- **Отговорности:**
  - UI/UX development (HTML, CSS, JavaScript)
  - Dashboard visualization
  - Responsive design
  - Chart.js integration

#### Diana Georgieva - Програмист, софтуерни приложения
- **Часове:** 8 часа/ден
- **Email:** zhorova1186@gmail.com
- **Роля:** Data Processing Developer
- **Отговорности:**
  - Data processing pipelines
  - Data validation
  - Analytics algorithms
  - Testing

#### Hristo Mishev - Програмист База Данни
- **Часове:** 4 часа/ден
- **Email:** hristo-mishev@proton.me
- **Роля:** Database Specialist
- **Отговорности:**
  - MySQL database design
  - Schema optimization
  - Query performance
  - Backups

#### Tsveta Popova - Програмист База Данни
- **Часове:** 4 часа/ден
- **Email:** ZvetaP@proton.me
- **Роля:** Data Quality Specialist
- **Отговорности:**
  - Data validation
  - Quality checks
  - SQL reporting
  - Data integrity

#### Maria Daleva - Мениджър, софтуерно развитие
- **Часове:** 4 часа/ден
- **Email:** mariq.d15@gmail.com
- **Роля:** Project Manager
- **Отговорности:**
  - Team coordination
  - Project documentation
  - Progress reporting
  - EU communication

**Total Team Capacity:** 32 часа/ден

---

## 4. TRL ROADMAP

### Technology Readiness Levels

#### TRL 3 (Юни-Юли 2025) - Концептуална валидация
**Цели:**
- Project setup и planning
- Basic prototypes
- Technology stack validation
- Initial API integration

**Deliverables:**
- Project plan документ
- Team roles definition
- GitHub repository setup
- Basic backend structure
- Initial UI mockups

**Status:** ✅ Завършен (30 Юли 2025)

---

#### TRL 4 (Август-Септември 2025) - Интеграция на компоненти
**Цели:**
- Component development
- Module integration
- Database implementation
- API endpoints creation
- Frontend-backend connection

**Deliverables:**
- Working Amazon API client
- Database schema implemented
- REST API endpoints functional
- Dashboard UI operational
- Integration tests

**Status:** ✅ Завършен (30 Септември 2025)

---

#### TRL 5 (Октомври 2025 - Февруари 2026) - Валидация в реална среда
**Цели:**
- Performance optimization
- Pilot testing с реални потребители
- User feedback collection
- Bug fixes и improvements
- Production readiness

**Deliverables:**
- Optimized system (API <100ms, UI <2s)
- 5 pilot users testing
- User manual
- Testing reports
- TRL 5 validation document

**Status:** ✅ Завършен (19 Февруари 2026)

---

#### TRL 6-7 (Март-Декември 2026) - Демонстрация и deployment
**Цели:**
- Production environment deployment
- Marketing materials
- Customer acquisition
- Continuous improvement
- TRL 7 finalization

**Status:** 🔄 Планиран (бъдещ фокус)

---

## 5. TIMELINE

```
2025
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Юни       ██████ TRL 3 Start
Юли       ██████ TRL 3 → TRL 4
Август    ██████ TRL 4 Development
Септ      ██████ TRL 4 Integration
Окт       ██████ TRL 4 → TRL 5
Ноем      ██████ TRL 5 Pilot Testing
Дек       ██████ TRL 5 Validation

2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ян-Февр   ██████ TRL 5 Finalization
Март-Юни  ██████ TRL 6 Development
Юли-Дек   ██████ TRL 7 Demonstration
```

---

## 6. BUDGET TRACKING

### Разпределение
- **Заплати:** 240,000 BGN (80.6%)
- **Оборудване:** 30,000 BGN (10.1%)
- **Услуги:** 20,000 BGN (6.7%)
- **Други:** 7,600 BGN (2.6%)

### Utilization (към 19 Февруари 2026)
- **Изразходвани:** 172,608 BGN (58%)
- **Останали:** 124,992 BGN (42%)
- **Status:** ✅ On track

---

## 7. РИСКОВЕ

### Идентифицирани рискове

| Риск | Вероятност | Въздействие | Mitigation |
|------|------------|-------------|------------|
| Amazon API rate limits | Средна | Високо | Caching, throttling |
| Team unavailability | Ниска | Средно | Cross-training |
| Budget overrun | Ниска | Високо | Weekly tracking |
| TRL delay | Средна | Високо | Buffer time |
| Data quality | Средна | Средно | Validation layers |

---

## 8. SUCCESS METRICS

### KPIs

**Technical:**
- ✅ API response time <100ms (achieved: 45ms)
- ✅ Dashboard load <2s (achieved: 1.4s)
- ✅ Test coverage >75% (achieved: 78%)
- ✅ Zero critical bugs (achieved: 0)

**Business:**
- ✅ 5 pilot users (achieved: 5)
- ✅ SUS score >70 (achieved: 78)
- ✅ User satisfaction >4.0/5 (achieved: 4.2)
- ✅ TRL 5 validation (achieved: ✅)

---

## 9. NEXT STEPS

### Immediate (Февруари-Март 2026)
- [ ] EU одит preparation
- [ ] Final documentation review
- [ ] Presentation materials
- [ ] TRL 6 planning

### Short-term (Април-Юни 2026)
- [ ] Production deployment
- [ ] Marketing campaign
- [ ] Customer onboarding
- [ ] Feature expansion

---

**Документ поддържан от:** Мария Далева  
**Последна актуализация:** 19 Февруари 2026  
**Статус на проект:** ✅ TRL 5 Validated, Ready за одит
