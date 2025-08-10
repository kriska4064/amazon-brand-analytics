// Chart Configuration - Създадено от Кристина Тодорова
// Дата: 10 Август 2025

// Brand colors за charts
const chartColors = {
    primary: '#FF9900',
    secondary: '#232F3E',
    success: '#36B37E',
    danger: '#DE350B',
    warning: '#FFAB00',
    info: '#6554C0',
    accent: '#00B8D9'
};

// Default chart configuration
const chartDefaults = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
            labels: {
                padding: 15,
                font: {
                    family: 'Open Sans',
                    size: 12
                },
                usePointStyle: true,
                boxWidth: 8
            }
        },
        tooltip: {
            backgroundColor: 'rgba(35, 47, 62, 0.95)',
            padding: 12,
            cornerRadius: 4,
            titleFont: {
                size: 14,
                weight: 'bold',
                family: 'Open Sans'
            },
            bodyFont: {
                size: 13,
                family: 'Open Sans'
            },
            displayColors: true,
            boxPadding: 6
        }
    },
    interaction: {
        intersect: false,
        mode: 'index'
    }
};

// Example: Rankings Trend Chart
function createRankingsChart(ctx) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ден 1', 'Ден 2', 'Ден 3', 'Ден 4', 'Ден 5', 'Ден 6', 'Ден 7'],
            datasets: [{
                label: 'Средна позиция',
                data: [15, 13, 14, 11, 10, 12, 9],
                borderColor: chartColors.primary,
                backgroundColor: chartColors.primary + '20',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: '#FFFFFF',
                pointBorderColor: chartColors.primary,
                pointBorderWidth: 2
            }]
        },
        options: {
            ...chartDefaults,
            scales: {
                y: {
                    reverse: true,
                    beginAtZero: false,
                    min: 1,
                    grid: {
                        color: '#E5E5E5',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            size: 12,
                            family: 'Open Sans'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Позиция (по-ниска е по-добра)',
                        font: {
                            size: 11,
                            family: 'Open Sans'
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12,
                            family: 'Open Sans'
                        }
                    }
                }
            }
        }
    });
}

// Example: Category Distribution Chart
function createCategoryChart(ctx) {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Electronics', 'Home & Kitchen', 'Sports', 'Beauty', 'Books'],
            datasets: [{
                data: [35, 25, 20, 15, 5],
                backgroundColor: [
                    chartColors.primary,
                    chartColors.info,
                    chartColors.success,
                    chartColors.accent,
                    chartColors.warning
                ],
                borderWidth: 2,
                borderColor: '#FFFFFF'
            }]
        },
        options: {
            ...chartDefaults,
            cutout: '60%',
            plugins: {
                ...chartDefaults.plugins,
                legend: {
                    ...chartDefaults.plugins.legend,
                    position: 'right'
                }
            }
        }
    });
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        chartColors,
        chartDefaults,
        createRankingsChart,
        createCategoryChart
    };
}
