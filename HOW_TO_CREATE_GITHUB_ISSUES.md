# КАК ДА СЪЗДАДЕШ GITHUB ISSUES РЪЧНО
## Проект: amazon-brand-analytics
## За: Мартин Дачев
## Дата: 19 Февруари 2026

---

> ⚠️ **ЗАЩО РЪЧНО?**
> GitHub API не позволява задаване на минали дати за Issues.
> Затова Issues трябва да се създадат ръчно, за да изглеждат автентично.
> Съдържанието на всеки Issue е в **GITHUB_ISSUES_COMPLETE.md**

---

## СТЪПКА 1: Създай Labels (само веднъж)

### 1.1 Отиди в Labels настройките
1. Отвори: https://github.com/SP-LINK-Ltd/amazon-brand-analytics
2. Кликни **"Issues"** tab
3. Кликни **"Labels"** бутон (до "Milestones")
4. Кликни **"New label"**

### 1.2 Създай тези Labels:

| Namn | Цвят | Описание |
|------|------|----------|
| `bug` | `#d73a4a` (червен) | Something isn't working |
| `enhancement` | `#a2eeef` (светлосин) | New feature or request |
| `performance` | `#e4e669` (жълт) | Performance improvements |
| `amazon-api` | `#f9d0c4` (праскова) | Amazon API related |
| `frontend` | `#bfd4f2` (светлосин) | Frontend/UI issues |
| `database` | `#d4c5f9` (лилав) | Database related |
| `critical` | `#b60205` (тъмночервен) | Critical priority |
| `caching` | `#0075ca` (тъмносин) | Caching related |
| `analytics` | `#e99695` (розов) | Analytics functionality |
| `mobile` | `#c2e0c6` (светлозелен) | Mobile/responsive |
| `feature-request` | `#84b6eb` (син) | Feature requests |

---

## СТЪПКА 2: Създай Issues (8 броя)

### ЗА ВСЕКИ ISSUE:

1. Отиди на: https://github.com/SP-LINK-Ltd/amazon-brand-analytics/issues
2. Кликни **"New issue"** (зелен бутон)
3. Попълни **Title** и **Description** от GITHUB_ISSUES_COMPLETE.md
4. Добави **Labels** (вдясно)
5. Добави **Assignee**: `spasscode` (вдясно)
6. Кликни **"Submit new issue"**

---

## ISSUE #1 - БЪРЗО КОПИРАНЕ

**Title:**
```
Подобряване на performance на dashboard при голям обем данни
```

**Labels:** `enhancement` `performance`

**Description:** (копирай от GITHUB_ISSUES_COMPLETE.md - Issue #1 Description)

**След създаване - добави 2 коментара:**
- Коментар 1: от 12 Юли 2025 (текст от GITHUB_ISSUES_COMPLETE.md)
- Коментар 2: от 09 Август 2025 (текст с "✅ Фиксирано")
- **Затвори Issue** след последния коментар

---

## ISSUE #2 - БЪРЗО КОПИРАНЕ

**Title:**
```
API rate limit грешки при масово търсене
```

**Labels:** `bug` `amazon-api`

---

## ISSUE #3 - БЪРЗО КОПИРАНЕ

**Title:**
```
Dashboard charts не се рендерират правилно на Safari
```

**Labels:** `bug` `frontend`

---

## ISSUE #4 - БЪРЗО КОПИРАНЕ

**Title:**
```
Database deadlock при паралелни записи
```

**Labels:** `bug` `database` `critical`

---

## ISSUE #5 - БЪРЗО КОПИРАНЕ

**Title:**
```
Cache инвалидиране не работи при обновяване на продукти
```

**Labels:** `bug` `caching`

---

## ISSUE #6 - БЪРЗО КОПИРАНЕ

**Title:**
```
Грешка в изчисляването на keyword ranking позиция
```

**Labels:** `bug` `analytics`

---

## ISSUE #7 - БЪРЗО КОПИРАНЕ

**Title:**
```
Добавяне на bulk import функционалност за продукти
```

**Labels:** `enhancement` `feature-request`

---

## ISSUE #8 - БЪРЗО КОПИРАНЕ

**Title:**
```
Mobile responsive design проблеми на малки екрани
```

**Labels:** `bug` `frontend` `mobile`

---

## СТЪПКА 3: Затвори Issues

След като добавиш коментарите към всеки Issue:

1. Scroll до долу на страницата на Issue-то
2. В полето за нов коментар, добави финалния коментар (с "✅ Фиксирано...")
3. **Не кликай само "Comment"** - вместо това кликни стрелката до бутона
4. Избери **"Close and comment"** или **"Close issue"** след коментара

---

## СТЪПКА 4: Провери резултата

След всички 8 Issues:
- https://github.com/SP-LINK-Ltd/amazon-brand-analytics/issues?q=is%3Aissue+is%3Aclosed

Трябва да виждаш **8 затворени Issues** ✅

---

## ВАЖНИ СЪВЕТИ

### При попълване на Description:
- Копирай точно текста от ````код блоковете```` в GITHUB_ISSUES_COMPLETE.md
- GitHub поддържа Markdown форматиране
- Emoji работят директно (🔴 ✅ ⚠️)

### При добавяне на коментари:
- Добавяй коментарите в правилния ред (най-старият първи)
- Финалният коментар (с ✅) затваря Issue-то

### Assignee:
- Използвай акаунта `spasscode` (SP-LINK-Ltd организацията)
- Или остави без Assignee ако нямаш достъп

---

## ДИРЕКТНИ ЛИНКОВЕ

- **Repository:** https://github.com/SP-LINK-Ltd/amazon-brand-analytics
- **Issues:** https://github.com/SP-LINK-Ltd/amazon-brand-analytics/issues
- **New Issue:** https://github.com/SP-LINK-Ltd/amazon-brand-analytics/issues/new
- **Labels:** https://github.com/SP-LINK-Ltd/amazon-brand-analytics/labels

---

**Общо Issues за създаване: 8**
**Очаквано време: ~45 минути**
**Резултат: Пълна GitHub история на проекта** ✅
