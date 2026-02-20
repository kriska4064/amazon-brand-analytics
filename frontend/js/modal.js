// Modal Component - Кристина Тодорова
function openModal(modalId) {
    const overlay = document.getElementById(modalId);
    if (overlay) { overlay.style.display = 'flex'; document.body.style.overflow = 'hidden'; }
}
function closeModal(modalId) {
    const overlay = document.getElementById(modalId);
    if (overlay) { overlay.style.display = 'none'; document.body.style.overflow = ''; }
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') document.querySelectorAll('.modal-overlay').forEach(m => m.style.display = 'none'); });
