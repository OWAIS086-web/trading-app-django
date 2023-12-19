// chart.js
document.addEventListener("DOMContentLoaded", function () {
    const userLabels = JSON.parse(document.getElementById("user-labels").textContent);
    const productCounts = JSON.parse(document.getElementById("product-counts").textContent);
  
    const ctx = document.getElementById("userProductChart").getContext("2d");
  
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: userLabels,
        datasets: [
          {
            label: "Number of Products",
            data: productCounts,
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  });
  