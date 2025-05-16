async function fetchCrimeData() {
  const res = await fetch("/api/trends");
  const data = await res.json();

  const ctx = document.getElementById('crimeChart').getContext('2d');
  const labels = [...new Set(Object.values(data).flatMap(city => Object.keys(city)).sort())];
  const datasets = Object.entries(data).map(([city, yearData]) => {
    return {
      label: city,
      data: labels.map(year => yearData[year] || 0),
      borderWidth: 1,
      fill: false
    };
  });

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Yearly Crime Trends by City'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  const summary = Object.entries(data).map(([city, stats]) => {
    const years = Object.keys(stats).sort();
    const diff = stats[years.at(-1)] - stats[years[0]];
    return `<p><strong>${city}:</strong> ${diff > 0 ? '⬆️' : '⬇️'} Crime ${diff > 0 ? 'increased' : 'decreased'} by ${Math.abs(diff)} since ${years[0]}</p>`;
  }).join("");

  document.getElementById("summary").innerHTML = summary;
}

window.onload = fetchCrimeData;
