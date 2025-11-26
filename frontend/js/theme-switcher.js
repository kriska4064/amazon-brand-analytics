// Theme Switcher - Кристина Тодорова
const THEME_KEY = 'amazon-analytics-theme';
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
}
function toggleTheme() {
    const current = localStorage.getItem(THEME_KEY) || 'light';
    applyTheme(current === 'dark' ? 'light' : 'dark');
}
document.addEventListener('DOMContentLoaded', () => {
    const saved = localStorage.getItem(THEME_KEY) || 'light';
    applyTheme(saved);
    const btn = document.getElementById('theme-toggle');
    if (btn) btn.addEventListener('click', toggleTheme);
});
