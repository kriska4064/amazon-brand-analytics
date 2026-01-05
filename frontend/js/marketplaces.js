/**
 * Marketplaces Configuration - TRL 5
 * Amazon Scanner marketplace selector with expanded countries
 * Author: Kristina Todorova
 */

const MARKETPLACES = [
  { id: 'US', name: 'USA', domain: 'amazon.com', flag: '🇺🇸', currency: 'USD', locale: 'en_US' },
  { id: 'DE', name: 'Germany', domain: 'amazon.de', flag: '🇩🇪', currency: 'EUR', locale: 'de_DE' },
  { id: 'CA', name: 'Canada', domain: 'amazon.ca', flag: '🇨🇦', currency: 'CAD', locale: 'en_CA' },
  { id: 'GB', name: 'United Kingdom', domain: 'amazon.co.uk', flag: '🇬🇧', currency: 'GBP', locale: 'en_GB' },
  { id: 'FR', name: 'France', domain: 'amazon.fr', flag: '🇫🇷', currency: 'EUR', locale: 'fr_FR' },
  { id: 'IT', name: 'Italy', domain: 'amazon.it', flag: '🇮🇹', currency: 'EUR', locale: 'it_IT' },
  { id: 'ES', name: 'Spain', domain: 'amazon.es', flag: '🇪🇸', currency: 'EUR', locale: 'es_ES' }
];

/**
 * Populate the marketplace dropdown selector
 * @param {string} selectId - DOM element ID of the select
 * @param {string|null} selectedId - pre-selected marketplace ID
 */
function populateMarketplaceDropdown(selectId, selectedId = 'US') {
  const select = document.getElementById(selectId);
  if (!select) return;

  select.innerHTML = '';
  const defaultOpt = document.createElement('option');
  defaultOpt.value = '';
  defaultOpt.textContent = '— Select Marketplace —';
  select.appendChild(defaultOpt);

  MARKETPLACES.forEach(mp => {
    const opt = document.createElement('option');
    opt.value = mp.id;
    opt.textContent = `${mp.flag} ${mp.name} (${mp.domain})`;
    opt.dataset.currency = mp.currency;
    opt.dataset.locale = mp.locale;
    if (mp.id === selectedId) opt.selected = true;
    select.appendChild(opt);
  });

  select.addEventListener('change', () => {
    const chosen = MARKETPLACES.find(m => m.id === select.value);
    if (chosen) {
      document.dispatchEvent(new CustomEvent('marketplaceChanged', { detail: chosen }));
    }
  });
}

/**
 * Get marketplace by ID
 * @param {string} id
 * @returns {Object|undefined}
 */
function getMarketplace(id) {
  return MARKETPLACES.find(m => m.id === id);
}

/**
 * Get currency symbol for marketplace
 */
function getCurrencySymbol(marketplaceId) {
  const symbols = { USD: '$', EUR: '€', GBP: '£', CAD: 'C$' };
  const mp = getMarketplace(marketplaceId);
  return mp ? (symbols[mp.currency] || mp.currency) : '$';
}

window.MARKETPLACES = MARKETPLACES;
window.populateMarketplaceDropdown = populateMarketplaceDropdown;
window.getMarketplace = getMarketplace;
window.getCurrencySymbol = getCurrencySymbol;
