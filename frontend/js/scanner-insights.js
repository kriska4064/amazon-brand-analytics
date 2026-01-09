/**
 * Scanner Insights Module - TRL 5
 * Keyword search, pagination, CSV export, marketplace filter, column sorting
 * Author: Kristina Todorova
 */

const ScannerInsights = (() => {
  let _allData = [];
  let _filtered = [];
  let _currentPage = 1;
  let _pageSize = 25;
  let _sortCol = null;
  let _sortDir = 'asc';
  let _activeMarketplace = null;
  let _searchTerm = '';

  // ── Initialise ──────────────────────────────────────────────────────────────
  function init() {
    _bindSearch();
    _bindMarketplaceFilter();
    _bindPageSizeSelector();
    _bindExportButtons();
    _bindSortableHeaders();
    populateMarketplaceDropdown('insights-marketplace-filter', null);
    document.addEventListener('marketplaceChanged', e => {
      _activeMarketplace = e.detail.id;
      _applyFilters();
    });
  }

  // ── Data Loading ─────────────────────────────────────────────────────────────
  function loadData(data) {
    _allData = Array.isArray(data) ? data : [];
    _currentPage = 1;
    _applyFilters();
  }

  // ── Filtering ────────────────────────────────────────────────────────────────
  function _applyFilters() {
    let result = [..._allData];

    if (_activeMarketplace) {
      result = result.filter(r => r.marketplace === _activeMarketplace);
    }

    if (_searchTerm) {
      const term = _searchTerm.toLowerCase();
      result = result.filter(r =>
        (r.keyword || '').toLowerCase().includes(term) ||
        (r.brand || '').toLowerCase().includes(term) ||
        (r.asin || '').toLowerCase().includes(term)
      );
    }

    if (_sortCol) {
      result.sort((a, b) => {
        const va = a[_sortCol] ?? '';
        const vb = b[_sortCol] ?? '';
        const cmp = typeof va === 'number' ? va - vb : String(va).localeCompare(String(vb));
        return _sortDir === 'asc' ? cmp : -cmp;
      });
    }

    _filtered = result;
    _currentPage = 1;
    _render();
    _renderPagination();
  }

  // ── Rendering ────────────────────────────────────────────────────────────────
  function _render() {
    const tbody = document.getElementById('scanner-insights-tbody');
    if (!tbody) return;

    const start = (_currentPage - 1) * _pageSize;
    const page = _filtered.slice(start, start + _pageSize);

    if (page.length === 0) {
      tbody.innerHTML = `<tr><td colspan="9" class="empty-msg">No results found.</td></tr>`;
      return;
    }

    tbody.innerHTML = page.map(row => {
      const mp = getMarketplace(row.marketplace);
      const sym = mp ? getCurrencySymbol(row.marketplace) : '$';
      const posClass = row.position <= 10 ? 'pos-top10' : row.position <= 30 ? 'pos-mid' : 'pos-low';
      return `<tr>
        <td>${mp ? mp.flag : ''} ${row.marketplace || '-'}</td>
        <td class="keyword-cell">${_esc(row.keyword || '-')}</td>
        <td>${_esc(row.brand || '-')}</td>
        <td>${_esc(row.asin || '-')}</td>
        <td class="${posClass}">${row.position || '-'}</td>
        <td>${row.sponsored ? '<span class="badge-sp">Sp</span>' : '<span class="badge-org">Org</span>'}</td>
        <td>${sym}${_fmt(row.price)}</td>
        <td>${_fmt(row.rating, 1)} ⭐</td>
        <td>${_fmtNum(row.reviews)}</td>
      </tr>`;
    }).join('');
  }

  function _renderPagination() {
    const container = document.getElementById('scanner-pagination');
    if (!container) return;

    const totalPages = Math.ceil(_filtered.length / _pageSize) || 1;
    const totalLabel = document.getElementById('scanner-total-count');
    if (totalLabel) totalLabel.textContent = `${_filtered.length} results`;

    let html = '';
    html += `<button onclick="ScannerInsights.goPage(1)" ${_currentPage === 1 ? 'disabled' : ''}>«</button>`;
    html += `<button onclick="ScannerInsights.goPage(${_currentPage - 1})" ${_currentPage === 1 ? 'disabled' : ''}>‹</button>`;

    const start = Math.max(1, _currentPage - 2);
    const end = Math.min(totalPages, _currentPage + 2);
    for (let p = start; p <= end; p++) {
      html += `<button onclick="ScannerInsights.goPage(${p})" class="${p === _currentPage ? 'active' : ''}">${p}</button>`;
    }

    html += `<button onclick="ScannerInsights.goPage(${_currentPage + 1})" ${_currentPage === totalPages ? 'disabled' : ''}>›</button>`;
    html += `<button onclick="ScannerInsights.goPage(${totalPages})" ${_currentPage === totalPages ? 'disabled' : ''}>»</button>`;

    container.innerHTML = html;
  }

  // ── Public API ───────────────────────────────────────────────────────────────
  function goPage(p) {
    const totalPages = Math.ceil(_filtered.length / _pageSize) || 1;
    _currentPage = Math.max(1, Math.min(p, totalPages));
    _render();
    _renderPagination();
  }

  function sortBy(col) {
    if (_sortCol === col) {
      _sortDir = _sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      _sortCol = col;
      _sortDir = 'asc';
    }
    _applyFilters();
    _updateSortIcons(col);
  }

  // ── CSV Export ───────────────────────────────────────────────────────────────
  function exportCurrentCSV() {
    _downloadCSV(_filtered, 'scanner_insights_filtered.csv');
  }

  function exportAllCSV() {
    _downloadCSV(_allData, 'scanner_insights_all.csv');
  }

  function _downloadCSV(data, filename) {
    if (!data.length) { alert('No data to export.'); return; }
    const cols = Object.keys(data[0]);
    const rows = [cols.join(',')];
    data.forEach(row => {
      rows.push(cols.map(c => `"${String(row[c] ?? '').replace(/"/g, '""')}"`).join(','));
    });
    const blob = new Blob([rows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename; a.click();
    URL.revokeObjectURL(url);
  }

  // ── Bindings ─────────────────────────────────────────────────────────────────
  function _bindSearch() {
    const input = document.getElementById('scanner-keyword-search');
    const btn = document.getElementById('scanner-search-btn');
    if (input) {
      input.addEventListener('keydown', e => { if (e.key === 'Enter') { _searchTerm = input.value.trim(); _applyFilters(); } });
    }
    if (btn) {
      btn.addEventListener('click', () => { _searchTerm = (document.getElementById('scanner-keyword-search') || {}).value?.trim() || ''; _applyFilters(); });
    }
  }

  function _bindMarketplaceFilter() {
    const sel = document.getElementById('insights-marketplace-filter');
    if (sel) sel.addEventListener('change', () => { _activeMarketplace = sel.value || null; _applyFilters(); });
  }

  function _bindPageSizeSelector() {
    const sel = document.getElementById('scanner-page-size');
    if (sel) sel.addEventListener('change', () => { _pageSize = parseInt(sel.value) || 25; _currentPage = 1; _render(); _renderPagination(); });
  }

  function _bindExportButtons() {
    const btnCurrent = document.getElementById('btn-export-current-csv');
    const btnAll = document.getElementById('btn-export-all-csv');
    if (btnCurrent) btnCurrent.addEventListener('click', exportCurrentCSV);
    if (btnAll) btnAll.addEventListener('click', exportAllCSV);
  }

  function _bindSortableHeaders() {
    document.querySelectorAll('[data-sort-col]').forEach(th => {
      th.style.cursor = 'pointer';
      th.addEventListener('click', () => sortBy(th.dataset.sortCol));
    });
  }

  function _updateSortIcons(activeCol) {
    document.querySelectorAll('[data-sort-col]').forEach(th => {
      const icon = th.querySelector('.sort-icon');
      if (!icon) return;
      if (th.dataset.sortCol === activeCol) {
        icon.textContent = _sortDir === 'asc' ? ' ▲' : ' ▼';
      } else {
        icon.textContent = ' ⇅';
      }
    });
  }

  // ── Helpers ──────────────────────────────────────────────────────────────────
  function _esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
  function _fmt(n, dec = 2) { return n != null ? Number(n).toFixed(dec) : '-'; }
  function _fmtNum(n) { return n != null ? Number(n).toLocaleString() : '-'; }

  return { init, loadData, goPage, sortBy, exportCurrentCSV, exportAllCSV };
})();

document.addEventListener('DOMContentLoaded', () => ScannerInsights.init());
window.ScannerInsights = ScannerInsights;
