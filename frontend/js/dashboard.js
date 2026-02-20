/**
 * Dashboard Графики
 * Автор: Кристина Тодорова
 */

// График за Тренд на Класиране
function loadRankingChart() {
    const ctx = document.getElementById('rankingChart').getContext('2d');
    
    // Примерни данни - TODO: Замени с реални данни от API
    const data = {
        labels: ['Седмица 1', 'Седмица 2', 'Седмица 3', 'Седмица 4'],
        datasets: [{
            label: 'Средна Позиция',
            data: [15, 13, 11, 12],
            borderColor: 'rgb(102, 126, 234)',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            tension: 0.4
        }]
    };
    
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    reverse: true, // По-ниско число на позиция е по-добре
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Позиция'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Период'
                    }
                }
            }
        }
    });
}

// График за Разпределение на Ключови Думи
function loadKeywordChart() {
    const ctx = document.getElementById('keywordChart').getContext('2d');
    
    // Примерни данни - TODO: Замени с реални данни от API
    const data = {
        labels: ['Топ 10', 'Страница 1 (11-20)', 'Страница 2', 'Страница 3+'],
        datasets: [{
            label: 'Брой Ключови Думи',
            data: [18, 12, 10, 5],
            backgroundColor: [
                'rgba(72, 187, 120, 0.8)',
                'rgba(102, 126, 234, 0.8)',
                'rgba(237, 137, 54, 0.8)',
                'rgba(245, 101, 101, 0.8)'
            ]
        }]
    };
    
    new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: false
                }
            }
        }
    });
}

// Зареди данни за графики от API
async function loadCharts(chartData) {
    if (!chartData) {
        console.log('Няма данни за графики, използваме примерни данни');
        return;
    }
    
    // TODO: Имплементирай зареждане на реални данни
    console.log('Зареждане на данни за графики:', chartData);
}
