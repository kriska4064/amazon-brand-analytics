/**
 * Amazon Brand Analytics - Frontend JavaScript
 * Connects to backend API with fallback to demo data
 */

const API_BASE = 'http://localhost:5000/api';

// State management
const state = {
    currentBrand: null,
    brands: [],
    charts: {},
    dateRange: 30,
    isLoading: false
};

// ===== INITIALIZATION =====

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    loadBrands();
    initKeyboardShortcuts();
});

// ===== API CALLS =====

async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        state.isLoading = true;
        showLoading(true);
        
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        
        if (data) options.body = JSON.stringify(data);
        
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
        
    } catch (error) {
        console.error(`API call failed (${endpoint}):`, error);
        showToast(`Грешка при зареждане. Показват се демо данни.`, 'warning');
        return null;
    } finally {
        state.isLoading = false;
        showLoading(false);
    }
}

// ===== DASHBOARD =====

async function loadDashboard() {
    const range = document.getElementById('dateRange')?.value || 30;
    state.dateRange = parseInt(range);
    
    const data = await apiCall(`/brands?page=1&per_page=5`) || getDemoData();
    
    updateKPIs(data);
    renderBrandsTable(data.brands || []);
    initCharts(data);
}

function updateKPIs(data) {
    const kpis = {
        'visibility-score': data.visibility_score?.toFixed(1) || '72.4',
        'visibility-change': data.visibility_change || '+5.2%',
        'keywords-tracked': data.total_keywords || '248',
        'keywords-change': '+12 нови',
        'avg-ranking': data.avg_position?.toFixed(1) || '8.3',
        'ranking-change': '↑ +2.1 позиции',
        'products-count': data.total || '47',
        'products-change': '+3 новодобавени'
    };
    
    Object.entries(kpis).forEach(([id, value]) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    });
}

function renderBrandsTable(brands) {
    const tbody = document.getElementById('brands-table-body');
    if (!tbody) return;
    
    if (brands.length === 0) {
        // Use demo data
        brands = getDemoBrands();
    }
    
    tbody.innerHTML = brands.map(brand => `
        <tr>
            <td><strong>${brand.name}</strong></td>
            <td>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${brand.visibility || 0}%"></div>
                    <span>${brand.visibility || 0}%</span>
                </div>
            </td>
            <td>${brand.keywords || 0}</td>
            <td>${brand.avg_position || '--'}</td>
            <td>
                <span class="trend-badge ${brand.trend || 'stable'}">
                    ${getTrendIcon(brand.trend)} ${brand.trend || 'stable'}
                </span>
            </td>
            <td>
                <button class="btn-action" onclick="viewBrand(${brand.id})">Виж</button>
            </td>
        </tr>
    `).join('');
}

function getTrendIcon(trend) {
    const icons = { improved: '↑', declined: '↓', stable: '→' };
    return icons[trend] || '→';
}

// ===== CHARTS =====

function initCharts(data) {
    initVisibilityChart(data);
    initMarketShareChart(data);
}

function initVisibilityChart(data) {
    const ctx = document.getElementById('visibility-chart');
    if (!ctx) return;
    
    if (state.charts.visibility) {
        state.charts.visibility.destroy();
    }
    
    const trendData = data.trend_data || getDemoTrendData();
    
    state.charts.visibility = new Chart(ctx, {
        type: 'line',
        data: {
            labels: trendData.map(d => d.date),
            datasets: [{
                label: 'Visibility Score',
                data: trendData.map(d => d.score),
                borderColor: '#4F46E5',
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `Score: ${ctx.raw.toFixed(1)}`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 0,
                    max: 100,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

function initMarketShareChart(data) {
    const ctx = document.getElementById('market-share-chart');
    if (!ctx) return;
    
    if (state.charts.marketShare) {
        state.charts.marketShare.destroy();
    }
    
    const shareData = data.market_share || getDemoMarketShare();
    
    state.charts.marketShare = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: shareData.map(d => d.brand),
            datasets: [{
                data: shareData.map(d => d.share),
                backgroundColor: ['#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 12 } } },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.label}: ${ctx.raw}%`
                    }
                }
            }
        }
    });
}

function changeChartType(chartName, type) {
    document.querySelectorAll('.btn-chart-type').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    if (state.charts[chartName]) {
        state.charts[chartName].config.type = type;
        state.charts[chartName].update();
    }
}

// ===== BRANDS MANAGEMENT =====

async function loadBrands() {
    const data = await apiCall('/brands') || { brands: getDemoBrands() };
    state.brands = data.brands || [];
    
    const brandsGrid = document.getElementById('brands-list');
    if (!brandsGrid) return;
    
    if (state.brands.length === 0) {
        brandsGrid.innerHTML = '<div class="no-data">Няма добавени брандове. Добавете вашия първи бранд!</div>';
        return;
    }
    
    brandsGrid.innerHTML = state.brands.map(brand => `
        <div class="brand-card" onclick="viewBrand(${brand.id})">
            <h3>${brand.name}</h3>
            <p class="brand-store">${brand.amazon_store_id || ''}</p>
            <div class="brand-score">
                <span>Visibility: ${brand.visibility || 0}%</span>
            </div>
        </div>
    `).join('');
}

function showAddBrandModal() {
    const modal = document.getElementById('add-brand-modal');
    if (modal) modal.style.display = 'flex';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

async function createBrand() {
    const name = document.getElementById('brand-name')?.value?.trim();
    const storeId = document.getElementById('brand-store-id')?.value?.trim();
    const category = document.getElementById('brand-category')?.value?.trim();
    const description = document.getElementById('brand-description')?.value?.trim();
    
    if (!name || !storeId) {
        showToast('Моля въведете задължителните полета', 'error');
        return;
    }
    
    const brandData = { name, amazon_store_id: storeId, category, description };
    
    const result = await apiCall('/brands', 'POST', brandData);
    
    if (result) {
        showToast(`Брандът "${name}" е добавен успешно!`, 'success');
        closeModal('add-brand-modal');
        loadBrands();
        loadDashboard();
    } else {
        // Demo mode
        state.brands.push({ id: Date.now(), name, amazon_store_id: storeId, visibility: 0 });
        showToast(`Брандът "${name}" е добавен (demo режим)`, 'success');
        closeModal('add-brand-modal');
        loadBrands();
    }
    
    // Clear form
    ['brand-name', 'brand-store-id', 'brand-category', 'brand-description'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
    });
}

function viewBrand(brandId) {
    showSection('dashboard');
    showToast(`Зареждане на данни за бранд #${brandId}...`, 'success');
}

// ===== KEYWORD ANALYSIS =====

async function searchKeyword() {
    const keyword = document.getElementById('keyword-search')?.value?.trim();
    if (!keyword) {
        showToast('Въведете ключова дума за търсене', 'warning');
        return;
    }
    
    const results = await apiCall(`/products/search?keyword=${encodeURIComponent(keyword)}`);
    
    const container = document.getElementById('keyword-results');
    if (!container) return;
    
    const data = results || getDemoKeywordResults(keyword);
    
    container.innerHTML = `
        <div class="keyword-header">
            <h3>Резултати за: "${keyword}"</h3>
            <span>${data.total || 0} резултата</span>
        </div>
        <div class="keyword-grid">
            ${(data.products || []).map(p => `
                <div class="keyword-card">
                    <strong>${p.title || 'Продукт'}</strong>
                    <span>Позиция: ${p.position || '--'}</span>
                    <span>ASIN: ${p.asin || '--'}</span>
                </div>
            `).join('') || '<p class="no-data">Въведете ключова дума за анализ</p>'}
        </div>
    `;
}

// ===== EXPORT =====

async function exportData(format) {
    showToast(`Подготовка на ${format.toUpperCase()} файл...`, 'success');
    // Placeholder for actual export
}

async function generateReport(type) {
    showToast(`Генериране на ${type.toUpperCase()} отчет...`, 'success');
}

// ===== SETTINGS =====

function saveSettings() {
    const settings = {
        access_key: document.getElementById('api-access-key')?.value,
        partner_tag: document.getElementById('partner-tag')?.value,
        region: document.getElementById('aws-region')?.value
    };
    
    localStorage.setItem('amazon_analytics_settings', JSON.stringify(settings));
    showToast('Настройките са запазени!', 'success');
}

// ===== NAVIGATION =====

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
    
    const section = document.getElementById(`section-${sectionId}`);
    if (section) section.classList.add('active');
    
    const menuItem = document.querySelector(`[data-section="${sectionId}"]`);
    if (menuItem) menuItem.classList.add('active');
}

function refreshData() {
    loadDashboard();
    showToast('Данните са обновени', 'success');
}

function logout() {
    if (confirm('Сигурни ли сте, че искате да излезете?')) {
        showToast('Излизане...', 'success');
    }
}

// ===== KEYBOARD SHORTCUTS =====

function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        if (e.altKey) {
            switch(e.key) {
                case '1': showSection('dashboard'); break;
                case '2': showSection('brands'); break;
                case '3': showSection('keywords'); break;
                case '4': showSection('competitors'); break;
                case '5': showSection('reports'); break;
                case 'r': refreshData(); break;
            }
        }
    });
}

// ===== UI HELPERS =====

function showLoading(show) {
    const indicator = document.getElementById('loading-indicator');
    if (indicator) indicator.style.display = show ? 'block' : 'none';
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===== DEMO DATA =====

function getDemoData() {
    return {
        brands: getDemoBrands(),
        visibility_score: 72.4,
        visibility_change: '+5.2%',
        total_keywords: 248,
        avg_position: 8.3,
        total: 47,
        trend_data: getDemoTrendData(),
        market_share: getDemoMarketShare()
    };
}

function getDemoBrands() {
    return [
        { id: 1, name: 'TechGear Pro', amazon_store_id: 'B001TECH', visibility: 78, keywords: 42, avg_position: 6.2, trend: 'improved' },
        { id: 2, name: 'SmartHome Plus', amazon_store_id: 'B002SMART', visibility: 65, keywords: 38, avg_position: 9.1, trend: 'stable' },
        { id: 3, name: 'EcoLife Brand', amazon_store_id: 'B003ECO', visibility: 54, keywords: 29, avg_position: 12.4, trend: 'declined' },
        { id: 4, name: 'FitnessPro', amazon_store_id: 'B004FIT', visibility: 82, keywords: 55, avg_position: 4.8, trend: 'improved' },
        { id: 5, name: 'HomeDecor Co', amazon_store_id: 'B005HOME', visibility: 61, keywords: 33, avg_position: 10.2, trend: 'stable' }
    ];
}

function getDemoTrendData() {
    const days = 30;
    const data = [];
    let score = 65;
    
    for (let i = days; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        score += (Math.random() - 0.45) * 3;
        score = Math.max(40, Math.min(100, score));
        
        data.push({
            date: date.toLocaleDateString('bg-BG', { month: 'short', day: 'numeric' }),
            score: parseFloat(score.toFixed(1))
        });
    }
    return data;
}

function getDemoMarketShare() {
    return [
        { brand: 'Нашият бранд', share: 28 },
        { brand: 'Конкурент A', share: 22 },
        { brand: 'Конкурент B', share: 18 },
        { brand: 'Конкурент C', share: 15 },
        { brand: 'Други', share: 17 }
    ];
}

function getDemoKeywordResults(keyword) {
    return {
        keyword,
        total: 10,
        products: Array.from({length: 5}, (_, i) => ({
            asin: `B00${Math.random().toString(36).substring(2, 7).toUpperCase()}`,
            title: `${keyword} - Продукт ${i + 1}`,
            position: i + 1
        }))
    };
}

// Обновление: 02.08.2025
// Имплементирани реални API извиквания заместващи mock данни
// Добавена обработка на грешки с fallback към demo данни
// Създадена функционалност за създаване на бранд
// Интегрирано зареждане на dashboard данни от backend

// Обновление: 21.01.2026
// Имплементирани финални заявки от потребителите
// Подобрена visual consistency
// Оптимизирана mobile experience
// Добавени повече опции за персонализация

function personalizeSettings(userId) {
    const prefs = JSON.parse(localStorage.getItem(`prefs_${userId}`) || '{}');
    return prefs;
}

function savePersonalization(userId, settings) {
    localStorage.setItem(`prefs_${userId}`, JSON.stringify(settings));
    showToast('Персонализацията е запазена', 'success');
}

// Brand card click handler - navigate to brand details
document.addEventListener('click', function(e) {
  const card = e.target.closest('.brand-card');
  if (card && card.dataset.brandId) {
    window.location.href = `brand-detail.html?id=${card.dataset.brandId}`;
  }
});
