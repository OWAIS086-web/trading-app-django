// Fetch data from the backend
fetch('/user_counts/')  // Update this URL to match your Django URL pattern
    .then(response => response.json())
    .then(data => {
        const users = data.data;

        const labels = users.map(user => `${user.fname} ${user.lname}`);
        const timeFetching = users.map(user => user.count);

        const ctx = document.getElementById('userTimeFetchingChart').getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Time Fetching',
                    data: timeFetching,
                    backgroundColor: 'rgba(0, 123, 255, 0.8)',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Time Fetching'
                        }
                    }
                }
            }
        });
    });
