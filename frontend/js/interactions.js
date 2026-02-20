// Micro-interactions - Кристина Тодорова
document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const target = document.querySelector(a.getAttribute('href'));
            if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
        });
    });
    // Toast notifications
    window.showToast = (msg, type = 'info') => {
        const toast = document.createElement('div');
        toast.className = `message message-${type}`;
        toast.innerHTML = `<span class="message-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>${msg}`;
        toast.style.cssText = 'position:fixed;top:20px;right:20px;z-index:99999;min-width:300px;animation:fadeIn 0.3s';
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    };
});
