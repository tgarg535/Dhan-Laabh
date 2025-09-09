document.addEventListener('DOMContentLoaded', () => {
    console.log("Chart script started."); // 1. Check if the script is running at all.

    const historicalChartCtx = document.getElementById('historicalStockChart');
    const predictionChartCtx = document.getElementById('predictionStockChart');
    const stockSymbol = window.stockSymbol;

    // 2. Log the critical elements to see if they were found on the page.
    console.log("Stock Symbol:", stockSymbol);
    console.log("Historical Chart Canvas:", historicalChartCtx);
    console.log("Prediction Chart Canvas:", predictionChartCtx);

    // Only run if the chart canvas elements and symbol are on the page
    if (!historicalChartCtx || !predictionChartCtx || !stockSymbol) {
        console.error("Initialization failed: A required element or the stock symbol is missing. Aborting chart creation.");
        return; 
    }
    
    console.log("Initialization successful. Proceeding to create charts."); // 3. Confirm that the initial check passed.
    
    let historicalChart, predictionChart;

    const getThemeColors = () => {
        const isDarkMode = document.documentElement.classList.contains('dark');
        return {
            gridColor: isDarkMode ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
            textColor: isDarkMode ? '#E5E7EB' : '#374151',
            tooltipBg: isDarkMode ? '#1F2937' : '#FFFFFF',
            borderColor: isDarkMode ? '#22c55e' : '#16a34a',
            predictionBorderColor: isDarkMode ? '#38bdf8' : '#0ea5e9'
        };
    };
    
    const createHistoricalChart = (labels, data) => {
        console.log("Creating historical chart with", labels.length, "data points."); // 6. Confirm this function is called.
        const colors = getThemeColors();
        if (historicalChart) historicalChart.destroy();

        historicalChart = new Chart(historicalChartCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `${stockSymbol} Price`,
                    data: data,
                    borderColor: colors.borderColor,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.1
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { x: { ticks: { color: colors.textColor }, grid: { color: colors.gridColor, drawOnChartArea: false } }, y: { ticks: { color: colors.textColor, callback: (value) => `$${value.toFixed(2)}` }, grid: { color: colors.gridColor } } }, plugins: { legend: { display: false }, tooltip: { backgroundColor: colors.tooltipBg, titleColor: colors.textColor, bodyColor: colors.textColor, } } }
        });
    };

    const createPredictionChart = (labels, data) => {
        console.log("Creating prediction chart with", labels.length, "data points.");
        const colors = getThemeColors();
        if (predictionChart) predictionChart.destroy();

        predictionChart = new Chart(predictionChartCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `Predicted ${stockSymbol} Price`,
                    data: data,
                    borderColor: colors.predictionBorderColor,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 0,
                    borderDash: [5, 5],
                    tension: 0.1
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { x: { ticks: { color: colors.textColor }, grid: { color: colors.gridColor, drawOnChartArea: false } }, y: { ticks: { color: colors.textColor, callback: (value) => `$${value.toFixed(2)}` }, grid: { color: colors.gridColor } } }, plugins: { legend: { display: false }, tooltip: { backgroundColor: colors.tooltipBg, titleColor: colors.textColor, bodyColor: colors.textColor, } } }
        });
    };
    
    const fetchHistoricalData = async (period = '1y') => {
        console.log(`Fetching historical data for period: ${period}...`); // 4. Check if the fetch function is called.
        try {
            const response = await fetch(`/api/historical-data/${stockSymbol}?period=${period}`);
            if (!response.ok) throw new Error(`Network response was not ok: ${response.statusText}`);
            const data = await response.json();
            console.log("Historical API Data Received:", data); // 5. THIS IS THE MOST IMPORTANT STEP. See what the server sent.
            createHistoricalChart(data.dates, data.prices);
        } catch (error) {
            console.error('Failed to fetch historical data:', error);
        }
    };
    
    const fetchPredictionData = async () => {
        console.log("Fetching prediction data...");
        try {
            const response = await fetch(`/api/predict-future/${stockSymbol}`);
            if (!response.ok) throw new Error(`Network response was not ok: ${response.statusText}`);
            const data = await response.json();
            console.log("Prediction API Data Received:", data);
            createPredictionChart(data.dates, data.prices);
        } catch (error) {
            console.error('Failed to fetch prediction data:', error);
        }
    };

    const chartControls = document.getElementById('historical-chart-controls');
    if(chartControls) {
        chartControls.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') {
                chartControls.querySelectorAll('.chart-btn').forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');
                const period = e.target.dataset.period;
                fetchHistoricalData(period);
            }
        });
    }

    const themeToggleButton = document.getElementById('theme-toggle');
    if(themeToggleButton) {
        themeToggleButton.addEventListener('click', () => {
            setTimeout(() => {
                const activePeriod = document.querySelector('.chart-btn.active')?.dataset.period || '1y';
                fetchHistoricalData(activePeriod);
                fetchPredictionData();
            }, 100);
        });
    }

    fetchHistoricalData();
    fetchPredictionData();
});