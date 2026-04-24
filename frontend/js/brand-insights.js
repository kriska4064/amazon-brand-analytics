/**
 * Brand Insights Module - TRL 5 (NEW MODULE)
 * Displays comprehensive brand data: avg position, organic/sponsored split,
 * organic/sponsored avg price, listing count with % chart
 * Author: Kristina Todorova
 */

const BrandInsights = (() => {

  let _chart = null;

  function init() {
    document.addEventListener('brandInsightsData', e => render(e.detail));
  }

  /**
   * Main render function
   * @param {Object} brand - brand analytics object from API
   */
  function render(brand) {
    if (!brand) return;

    // KPI cards
    _setText('bi-brand-name', brand.name || '-');
    _setText('bi-total-listings', brand.totalListings || 0);
    _setText('bi-avg-position', _fmt(brand.avgPosition));
    _setText('bi-organic-avg-position', _fmt(brand.organicAvgPosition));
    _setText('bi-sponsored-avg-position', _fmt(brand.sponsoredAvgPosition));
    _setText('bi-avg-price', _fmtPrice(brand.avgPrice, brand.currency));
    _setText('bi-organic-avg-price', _fmtPrice(brand.organicAvgPrice, brand.currency));
    _setText('bi-sponsored-avg-price', _fmtPrice(brand.sponsoredAvgPrice, brand.currency));
    _setText('bi-marketplace', (getMarketplace(brand.marketplace) || {}).name || brand.marketplace);

    // Rank badges
    _renderRankBadge('bi-organic-rank', brand.organicRankLevel);
    _renderRankBadge('bi-sponsored-rank', brand.sponsoredRankLevel, true);

    // Listing distribution donut chart
    _renderListingsChart(brand);

    // Top keywords table
    _renderTopKeywords(brand.topKeywords || []);
  }

  function _renderRankBadge(elementId, level, isSponsored = false) {
    const el = document.getElementById(elementId);
    if (!el) return;
    const label = isSponsored ? 'Sponsored rank' : 'Organic rank';
    const config = {
      High:   { icon: '🟢', cls: 'rank-high' },
      Medium: { icon: '🟡', cls: 'rank-medium' },
      Low:    { icon: '🔴', cls: 'rank-low' }
    };
    const c = config[level] || { icon: '⚪', cls: '' };
    el.className = `rank-badge ${c.cls}`;
    el.innerHTML = `${c.icon} <strong>${label}:</strong> ${level || 'N/A'}`;
  }

  function _renderListingsChart(brand) {
    const canvas = document.getElementById('bi-listings-chart');
    if (!canvas) return;

    const organic = brand.organicListings || 0;
    const sponsored = brand.sponsoredListings || 0;
    const total = organic + sponsored;

    if (_chart) _chart.destroy();

    _chart = new Chart(canvas.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: [
          `Organic (${organic} listings – ${_pct(organic, total)}%)`,
          `Sponsored (${sponsored} listings – ${_pct(sponsored, total)}%)`
        ],
        datasets: [{
          data: [organic, sponsored],
          backgroundColor: ['#22c55e', '#f59e0b'],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom' },
          tooltip: {
            callbacks: {
              label: ctx => `${ctx.label}: ${ctx.parsed} listings (${_pct(ctx.parsed, total)}%)`
            }
          }
        }
      }
    });

    // Update text summary below chart
    _setText('bi-organic-count', `${organic} listings (${_pct(organic, total)}%)`);
    _setText('bi-sponsored-count', `${sponsored} listings (${_pct(sponsored, total)}%)`);
  }

  function _renderTopKeywords(keywords) {
    const tbody = document.getElementById('bi-keywords-tbody');
    if (!tbody) return;
    if (!keywords.length) {
      tbody.innerHTML = '<tr><td colspan="4">No keyword data available.</td></tr>';
      return;
    }
    tbody.innerHTML = keywords.slice(0, 20).map(kw => `
      <tr>
        <td>${_esc(kw.keyword)}</td>
        <td>${kw.position || '-'}</td>
        <td>${kw.sponsored ? '<span class="badge-sp">Sponsored</span>' : '<span class="badge-org">Organic</span>'}</td>
        <td>${_fmtPrice(kw.price, kw.currency)}</td>
      </tr>
    `).join('');
  }

  // ── Helpers ──────────────────────────────────────────────────────────────────
  function _setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  }
  function _esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function _fmt(n) { return n != null ? Number(n).toFixed(1) : '-'; }
  function _fmtPrice(n, currency) {
    if (n == null) return '-';
    const sym = currency === 'GBP' ? '£' : currency === 'CAD' ? 'C$' : currency === 'EUR' ? '€' : '$';
    return `${sym}${Number(n).toFixed(2)}`;
  }
  function _pct(part, total) { return total ? Math.round((part / total) * 100) : 0; }

  return { init, render };
})();

document.addEventListener('DOMContentLoaded', () => BrandInsights.init());
window.BrandInsights = BrandInsights;
