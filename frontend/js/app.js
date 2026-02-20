/**
 * Софтуер за Анализ на Брандове в Amazon - Главен JavaScript
 * Автор: Кристина Тодорова
 * Архитектура: Мартин Дачев
 */

// API Конфигурация
const API_BASE_URL = 'http://localhost:5000/api';

// Помощни Функции
const fetchAPI = async (endpoint, options = {}) => {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });
        
        if (!response.ok) {
            throw new Error(`HTTP грешка! статус: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Грешка:', error);
        return null;
    }
};

// Зареди dashboard данни при зареждане на страницата
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    setupNavigation();
});

// Навигация
function setupNavigation() {
    const navLinks = document.querySelectorAll('nav a');
    const sections = document.querySelectorAll('main section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            
            // Скрий всички секции
            sections.forEach(section => {
                section.style.display = 'none';
            });
            
            // Покажи целевата секция
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.style.display = 'block';
            }
        });
    });
}

// Зареди Dashboard
async function loadDashboard() {
    try {
        // Зареди показатели от API
        const response = await fetchAPI('/analytics/dashboard?brand_id=1');
        
        if (response) {
            updateMetrics(response.metrics);
            loadCharts(response.chart_data);
        }
    } catch (error) {
        console.error('Неуспешно зареждане на dashboard:', error);
        // Fallback към demo данни
        updateMetrics({
            avgPosition: 12.5,
            visibilityScore: 78.2,
            totalKeywords: 45,
            top10Count: 18
        });
    }
    
    // Зареди графики
    loadRankingChart();
    loadKeywordChart();
}

// Актуализирай Показатели
function updateMetrics(data) {
    document.getElementById('avg-position').textContent = data.avgPosition ? data.avgPosition.toFixed(1) : '-';
    document.getElementById('visibility-score').textContent = data.visibilityScore ? data.visibilityScore.toFixed(1) : '-';
    document.getElementById('total-keywords').textContent = data.totalKeywords || '-';
    document.getElementById('top10-count').textContent = data.top10Count || '-';
}

// Търси Ключови Думи
async function searchKeywords() {
    const searchInput = document.getElementById('keyword-search');
    const keyword = searchInput.value.trim();
    
    if (!keyword) {
        alert('Моля въведете ключова дума');
        return;
    }
    
    const data = await fetchAPI('/keywords/search', {
        method: 'POST',
        body: JSON.stringify({ keyword }),
    });
    
    if (data) {
        displayKeywordResults(data.резултати || data.results || []);
    }
}

// Покажи Резултати от Ключови Думи
function displayKeywordResults(results) {
    const tbody = document.getElementById('keywords-tbody');
    tbody.innerHTML = '';
    
    if (!results || results.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">Няма намерени резултати</td></tr>';
        return;
    }
    
    results.forEach(result => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${result.keyword || result.ключова_дума}</td>
            <td>${result.searchVolume || result.обем_на_търсене}</td>
            <td>${result.position || result.позиция}</td>
            <td>${result.trend || result.тенденция}</td>
            <td>${result.competition || result.конкуренция}</td>
        `;
    });
}

// Създай Бранд
async function createBrand(brandData) {
    const response = await fetchAPI('/brands', {
        method: 'POST',
        body: JSON.stringify(brandData)
    });
    
    if (response && !response.error && !response.грешка) {
        alert('Брандът е създаден успешно!');
        loadDashboard();
    } else {
        alert('Грешка при създаване на бранд: ' + (response?.error || response?.грешка || 'Неизвестна грешка'));
    }
}
