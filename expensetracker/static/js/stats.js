const renderChart = (labels, data) => {
    const ctx = document.getElementById('myChart');

    Chart.getChart("myChart")?.destroy();

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 Months Expenses',
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
            title: {
                display: true,
                text: 'Expense Per Summary',
            }
        }
        }
    });
};

const getStats = () => {
    fetch('/expense-category-summary')
        .then(res => res.json())
        .then(results => {
            const category_data = results.expense_category_data;

            if (!category_data || Object.keys(category_data).length === 0) {
                console.warn("No data found for chart");
                return; //  don’t render a dummy chart
            }

            const [labels, data] = [
                Object.keys(category_data),
                Object.values(category_data)
            ];
            renderChart(labels, data);
        }
        );
};

document.addEventListener('DOMContentLoaded', getStats);