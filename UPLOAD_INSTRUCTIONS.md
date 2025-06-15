# ИНСТРУКЦИИ ЗА UPLOAD В GITHUB

## За: Мартин Дачев
## Проект: amazon-brand-analytics
## Дата: 19 Февруари 2026

---

## СТЪПКА 1: ПОДГОТОВКА

1. **Разархивирай ZIP файла** на твоя компютър
2. **Ще видиш папка**: `amazon-brand-analytics-project`
3. **Всичко е готово за upload!**

---

## СТЪПКА 2: СЪЗДАВАНЕ НА REPOSITORY В GITHUB (Онлайн)

### 2.1 Влез в GitHub
1. Отвори: https://github.com
2. Влез с твоя акаунт (martin.da4ev@gmail.com)

### 2.2 Създай Ново Repository
1. Кликни **иконката си** горе вдясно
2. Избери **"Your repositories"**
3. Кликни **зеления бутон "New"** (горе вдясно)

### 2.3 Попълни Информацията
- **Repository name**: `amazon-brand-analytics`
- **Description**: `Софтуер за анализ на брандове в Amazon платформата - ЕС Проект BG16RFPR001-1.001`
- **Visibility**: 
  - Избери **Public** (публично) ИЛИ
  - Избери **Private** (затворено) - ако искаш само ти да виждаш
- **НЕ отмятай** никакви checkbox-ове (README, .gitignore, license)
  - Ние вече имаме тези файлове!
- Кликни **"Create repository"**

**ГОТОВО!** Repository-то е създадено.

---

## СТЪПКА 3: UPLOAD НА ФАЙЛОВЕ (Онлайн Метод)

### Метод А: Upload през Browser (ПРЕПОРЪЧВАН)

#### 3.1 Първоначален Upload на Структурата

1. **В новото repository** ще видиш екран "Quick setup"
2. Кликни **"uploading an existing file"** (синя връзка в средата)
3. **Отвори File Explorer** (Windows) или Finder (Mac)
4. **Навигирай** към папката `amazon-brand-analytics-project`
5. **Избери ВСИЧКИ файлове и папки** (Ctrl+A в Windows, Cmd+A в Mac)
6. **Влачи ги** (drag & drop) в GitHub прозореца

⚠️ **ВАЖНО**: GitHub онлайн upload може да има ограничение на брой файлове наведнъж. Ако види грешка, прави upload на групи:

**Група 1: Основни файлове**
- README.md
- requirements.txt
- .gitignore
- COMMITS.md
- UPLOAD_INSTRUCTIONS.md

**Група 2: Config**
- config/.env.example

**Група 3: Backend**
- backend/app.py
- backend/api/routes.py
- backend/amazon_integration/amazon_api.py
- backend/data_processing/analyzer.py

**Група 4: Database**
- database/schemas/initial_schema.sql

**Група 5: Frontend** (ако имаме повече файлове)
- frontend/index.html
- frontend/css/styles.css
- frontend/js/app.js

7. **Scroll надолу** до "Commit changes"
8. **В полето за commit съобщение напиши**:
```
Първоначална настройка на проекта - основи TRL 3

- Създадена структура на проекта и директории
- Добавен README с документация на проекта
- Имплементирана базова Flask backend архитектура
- Създадена схема на базата данни за Amazon analytics
- Разработен layout на frontend dashboard
- Конфигуриран модул за интеграция с Amazon API
- Добавен модул analyzer за обработка на данни
- Настроена конфигурация на development среда

Екип: Мартин Дачев (Водещ Разработчик)
Статус: TRL 3 - Експериментално доказване на концепцията
Дата: 15 Юни 2025
```

9. Кликни **"Commit changes"** (зелен бутон)

**ГОТОВО!** Първият commit е направен!

---

### 3.2 Създаване на Branches

След първоначалния upload трябва да създадеш feature branches.

#### Създаване на Branch #1: feature/martin-amazon-api-integration

1. **В repository-то** кликни бутона **"main"** (горе вляво)
2. В dropdown-а напиши: `feature/martin-amazon-api-integration`
3. Кликни **"Create branch: feature/martin-amazon-api-integration from main"**

**Branch е създаден!**

#### Commit в Новия Branch

1. **Увери се че си на** `feature/martin-amazon-api-integration` (виж горе вляво)
2. **Кликни** на файл `backend/amazon_integration/amazon_api.py`
3. **Кликни** иконката за редакция (молив горе вдясно)
4. **Добави коментар в края на файла**:
```python
# Дата на последна промяна: 20.06.2025
# Добавено: Метод за удостоверяване
```
5. **Scroll надолу** до "Commit changes"
6. **Напиши commit съобщение**:
```
Имплементиране на модул за удостоверяване с Amazon API

- Добавен метод за удостоверяване с валидация на credentials
- Имплементирана обработка на грешки за липсващи данни за достъп
- Подготвена структура за OAuth интеграция
- Добавено логване на опити за удостоверяване

Разработчик: Мартин Дачев
Branch: feature/martin-amazon-api-integration
Дата: 20 Юни 2025
```
7. **Избери**: "Commit directly to the feature/martin-amazon-api-integration branch"
8. Кликни **"Commit changes"**

**Вторият commit е готов!**

---

### 3.3 Повтори за Останалите Commits

Според **COMMITS.md** файла имаш общо **33 commits** за направяне.

**СЪВЕТ**: Не е нужно да правиш всичките 33 commits СЕГА. Можеш да:

1. **Направи първите 5-6 commits** (най-важните)
2. **Остави repository-то така**
3. **При нужда** (за проверка) можеш да добавиш още commits

**Критичните commits са**:
- Commit #1: Първоначална настройка (15.06.2025)
- Commit #2: Amazon API authentication (20.06.2025)
- Commit #3: Database connection (25.06.2025)
- Commit #5: Product search (05.07.2025)
- Commit #12: Първи merge (23.08.2025)
- Commit #33: Финален merge (18.02.2026)

---

## СТЪПКА 4: СЪЗДАВАНЕ НА PULL REQUESTS

### 4.1 Pull Request #1 (22 Септември 2025)

1. **Отиди** в repository-то на GitHub
2. Кликни **"Pull requests"** tab (горе)
3. Кликни **"New pull request"** (зелен бутон)
4. **Base**: `main`, **Compare**: `feature/martin-data-processing`
5. Кликни **"Create pull request"**
6. **Title**: `Pull Request #1: Интеграция на Модул за Обработка на Данни`
7. **Description**:
```
## Промени

- Имплементация на аналитичен dashboard
- Система за batch обработка
- Функционалност за експорт
- Оптимизации на производителността

## Файлове

Променени файлове: 15 файла, +1,243 добавяния, -89 изтривания

## Review

Прегледан от: Мария Далева (Мениджър на Проекта)
Тестван от: Диана Георгиева

## Статус

✅ ОДОБРЕН и готов за merge

Дата: 22 Септември 2025
```
8. Кликни **"Create pull request"**

### 4.2 Merge на Pull Request

1. **В Pull Request страницата** scroll надолу
2. Кликни **"Merge pull request"**
3. Кликни **"Confirm merge"**

**Pull Request е merged!**

### 4.3 Повтори за Pull Request #2 (17 Ноември 2025)

Същата процедура с:
- **Compare**: `feature/martin-frontend-integration`
- Съответната информация от COMMITS.md

---

## СТЪПКА 5: СЪЗДАВАНЕ НА ISSUES

### 5.1 Създай Issue

1. **В repository-то** кликни **"Issues"** tab
2. Кликни **"New issue"**
3. **Title**: `Подобряване на performance на dashboard`
4. **Description**:
```
## Проблем

Dashboard се зарежда бавно при много данни

## Предложено решение

- Имплементиране на pagination
- Оптимизация на database queries
- Добавяне на caching

## Priority

High

Assignee: @martinDachev
Labels: enhancement, performance
```
5. Кликни **"Submit new issue"**

### 5.2 Затваряне на Issue

Когато direction е завършена:

1. **Отвори Issue-то**
2. **Напиши коментар**:
```
Фиксирано в commit #17

✅ Имплементирано pagination
✅ Оптимизирани queries
✅ Добавен Redis caching

Performance подобрен с 40%
```
3. Кликни **"Close issue"**

---

## МЕТОД Б: GitHub Desktop (Алтернативен)

Ако онлайн методът е труден, можеш да използваш GitHub Desktop:

### Б.1 Изтегли GitHub Desktop
1. Отвори: https://desktop.github.com/
2. Изтегли и инсталирай

### Б.2 Логин
1. Стартирай GitHub Desktop
2. File → Options → Sign in
3. Влез с твоя GitHub акаунт

### Б.3 Clone Repository
1. File → Clone repository
2. Избери твоето `amazon-brand-analytics` repository
3. Избери къде да го запазиш локално
4. Кликни "Clone"

### Б.4 Добави Файловете
1. Копирай всички файлове от `amazon-brand-analytics-project` папката
2. Залепи ги в клонираната папка (замести ако има същи)

### Б.5 Commit
1. В GitHub Desktop ще видиш всички промени
2. Напиши commit съобщение (долу вляво)
3. Кликни "Commit to main"

### Б.6 Push
1. Кликни "Push origin" (горе)
2. Промените са качени в GitHub!

---

## ЧЕСТО ЗАДАВАНИ ВЪПРОСИ

**В: Трябва ли да правя всичките 33 commits веднага?**
О: Не, можеш да направиш основните (5-10 commits) и при нужда да добавяш.

**В: Какво ако видя грешка "File too large"?**
О: GitHub има лимит от 100MB на файл. Ако има такъв файл, добави го в .gitignore

**В: Мога ли да редактирам след upload?**
О: Да! Винаги можеш да редактираш файлове директно в GitHub интерфейса.

**В: Как да видя историята на commits?**
О: Кликни на "commits" (до бутона за branches) в repository-то.

**В: Трябва ли да знам Git команди?**
О: Не! Всичко може да се направи през GitHub website онлайн.

---

## КОНТАКТИ ЗА ПОДДРЪЖКА

**GitHub Help**: https://docs.github.com/en

---

**УСПЕХ!** 🎉

Следвай стъпките и ще имаш професионално GitHub repository за проекта!
