// Onboarding Tour - Кристина Тодорова
const tourSteps = [
    { element: '.navbar-brand', title: 'Добре дошли!', text: 'Това е Amazon Brand Analytics dashboard.' },
    { element: '.dashboard-grid', title: 'KPI Cards', text: 'Тук виждате основните метрики на вашите брандове.' },
    { element: '.sidebar', title: 'Навигация', text: 'Използвайте менюто за достъп до всички секции.' }
];
let currentStep = 0;
function startTour() {
    currentStep = 0;
    showStep(currentStep);
}
function showStep(index) {
    const step = tourSteps[index];
    const el = document.querySelector(step.element);
    if (!el) return;
    const rect = el.getBoundingClientRect();
    console.log(`Tour step ${index + 1}: ${step.title}`);
}
window.startTour = startTour;
