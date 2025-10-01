const renderChart = (labels, data) => {
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'bar',
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
    console.log("Getting stats...");
    fetch('/expense-category-summary')
        .then(res => res.json())
        .then(results => {
            console.log("Results", results);

            renderChart([], []);
        }
        );
};

document.onload = getStats();
