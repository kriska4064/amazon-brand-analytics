/**
 * Competitor Insights Module - TRL 5 (NEW MODULE)
 * Compare up to 5 brands side-by-side with charts and tables
 * Author: Kristina Todorova
 */

const CompetitorInsights = (() => {
  const MAX_BRANDS = 5;
  let _selectedBrands = [];
  let _charts = {};

  function init() {
    document.addEventListener('DOMContentLoaded', _setup);
    document.addEventListener('competitorData', e => renderComparison(e.detail));
  }

  function _setup() {
    const addBtn = document.getElementById('ci-add-brand-btn');
    if (addBtn) addBtn.addEventListener('click', _handleAddBrand);
    const compareBtn = document.getElementById('ci-compare-btn');
    if (compareBtn) compareBtn.addEventListener('click', _triggerCompare);
    const clearBtn = document.getElementById('ci-clear-btn');
    if (clearBtn) clearBtn.addEventListener('click', _clearAll);
  }

  function _handleAddBrand() {
    const input = document.getElementById('ci-brand-input');
    if (!input) return;
    const name = input.value.trim();
    if (!name) return;
    if (_selectedBrands.length >= MAX_BRANDS) {
      alert(`You can compare up to ${MAX_BRANDS} brands.`); return;
    }
    if (_selectedBrands.includes(name)) {
      alert('Brand already added.'); return;
    }
    _selectedBrands.push(name);
    input.value = '';
    _renderSelectedBrandTags();
  }

  function _renderSelectedBrandTags() {
    const container = document.getElementById('ci-selected-brands');
    if (!container) return;
    container.innerHTML = _selectedBrands.map((b, i) =>
      `<span class="brand-tag">${b} <button onclick="CompetitorInsights.removeBrand(${i})">×</button></span>`
    ).join('');
    const compareBtn = document.getElementById('ci-compare-btn');
    if (compareBtn) compareBtn.disabled = _selectedBrands.length < 2;
  }

  function removeBrand(index) {
    _selectedBrands.splice(index, 1);
    _renderSelectedBrandTags();
  }

  function _triggerCompare() {
    if (_selectedBrands.length < 2) { alert('Select at least 2 brands.'); return; }
    document.dispatchEvent(new CustomEvent('competitorCompareRequest', { detail: { brands: [..._selectedBrands] } }));
  }

  function _clearAll() {
    _selectedBrands = [];
    _renderSelectedBrandTags();
    _destroyCharts();
    const section = document.getElementById('ci-results-section');
    if (section) section.style.display = 'none';
  }

  /**
   * Main render - called when API returns comparison data
   * @param {Array} brands - array of brand data objects
   */
  function renderComparison(brands) {
    if (!Array.isArray(brands) || !brands.length) return;

    _renderComparisonTable(brands);
    _renderVisibilityChart(brands);
    _renderPositionChart(brands);
    _renderPriceChart(brands);

    const section = document.getElementById('ci-results-section');
    if (section) section.style.display = 'block';
  }

  function _renderComparisonTable(brands) {
    const container = document.getElementById('ci-comparison-table-container');
    if (!container) return;

    const rows = [
      { label: 'Total Listings', key: 'totalListings', fmt: n => n },
      { label: 'Avg. Position', key: 'avgPosition', fmt: n => Number(n).toFixed(1) },
      { label: 'Organic Avg. Position', key: 'organicAvgPosition', fmt: n => Number(n).toFixed(1) },
      { label: 'Sponsored Avg. Position', key: 'sponsoredAvgPosition', fmt: n => Number(n).toFixed(1) },
      { label: 'Avg. Price', key: 'avgPrice', fmt: (n, b) => _fmtPrice(n, b.currency) },
      { label: 'Organic Avg. Price', key: 'organicAvgPrice', fmt: (n, b) => _fmtPrice(n, b.currency) },
      { label: 'Sponsored Avg. Price', key: 'sponsoredAvgPrice', fmt: (n, b) => _fmtPrice(n, b.currency) },
      { label: 'Organic Listings %', key: null, calc: b => `${_pct(b.organicListings, b.totalListings)}%` },
      { label: 'Advertising Aggressiveness', key: null, calc: b => _adAggressiveness(b.sponsoredListings, b.totalListings) },
      { label: 'Organic Strength', key: null, calc: b => _organicStrength(b.organicListings, b.totalListings, b.organicAvgPosition) },
      { label: 'Brand Visibility', key: 'visibilityScore', fmt: n => `${Number(n).toFixed(0)}%` }
    ];

    let html = `<table class="ci-table"><thead><tr><th>Metric</th>`;
    brands.forEach(b => { html += `<th>${_esc(b.name)}</th>`; });
    html += `</tr></thead><tbody>`;

    rows.forEach(row => {
      html += `<tr><td class="metric-label">${row.label}</td>`;
      brands.forEach(b => {
        let val;
        if (row.calc) val = row.calc(b);
        else val = row.fmt ? row.fmt(b[row.key], b) : b[row.key];
        html += `<td>${val ?? '-'}</td>`;
      });
      html += `</tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;
  }

  function _renderVisibilityChart(brands) {
    const canvas = document.getElementById('ci-visibility-chart');
    if (!canvas) return;
    if (_charts.visibility) _charts.visibility.destroy();
    _charts.visibility = new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: brands.map(b => b.name),
        datasets: [{
          label: 'Brand Visibility (%)',
          data: brands.map(b => b.visibilityScore || 0),
          backgroundColor: _palette(brands.length)
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, max: 100 } }
      }
    });
  }

  function _renderPositionChart(brands) {
    const canvas = document.getElementById('ci-position-chart');
    if (!canvas) return;
    if (_charts.position) _charts.position.destroy();
    _charts.position = new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: brands.map(b => b.name),
        datasets: [
          { label: 'Organic Avg. Position', data: brands.map(b => b.organicAvgPosition || 0), backgroundColor: '#22c55e' },
          { label: 'Sponsored Avg. Position', data: brands.map(b => b.sponsoredAvgPosition || 0), backgroundColor: '#f59e0b' }
        ]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
  }

  function _renderPriceChart(brands) {
    const canvas = document.getElementById('ci-price-chart');
    if (!canvas) return;
    if (_charts.price) _charts.price.destroy();
    _charts.price = new Chart(canvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: brands.map(b => b.name),
        datasets: [
          { label: 'Organic Avg. Price', data: brands.map(b => b.organicAvgPrice || 0), backgroundColor: '#6366f1' },
          { label: 'Sponsored Avg. Price', data: brands.map(b => b.sponsoredAvgPrice || 0), backgroundColor: '#ec4899' }
        ]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
  }

  function _destroyCharts() {
    Object.values(_charts).forEach(c => c && c.destroy());
    _charts = {};
  }

  // ── Business Logic ────────────────────────────────────────────────────────────
  function _adAggressiveness(sponsored, total) {
    if (!total) return '-';
    const ratio = (sponsored / total) * 100;
    if (ratio > 70) return '🔴 High';
    if (ratio >= 20) return '🟡 Medium';
    return '🟢 Low';
  }

  function _organicStrength(organic, total, organicPosition) {
    if (!total) return '-';
    const ratio = (organic / total) * 100;
    if (ratio >= 60 && organicPosition <= 60) return '🟢 Strong';
    if (ratio < 30 || organicPosition > 80) return '🔴 Weak';
    return '🟡 Medium';
  }

  // ── Helpers ──────────────────────────────────────────────────────────────────
  function _esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function _fmtPrice(n, currency) {
    if (n == null) return '-';
    const sym = { GBP: '£', CAD: 'C$', EUR: '€', USD: '$' }[currency] || '$';
    return `${sym}${Number(n).toFixed(2)}`;
  }
  function _pct(part, total) { return total ? Math.round((part / total) * 100) : 0; }
  function _palette(n) {
    const all = ['#6366f1','#22c55e','#f59e0b','#ec4899','#14b8a6'];
    return all.slice(0, n);
  }

  return { init, renderComparison, removeBrand };
})();

CompetitorInsights.init();
window.CompetitorInsights = CompetitorInsights;
