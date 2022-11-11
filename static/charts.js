function makeChartData(data) {
  return Array.from(data, e => e == null ? 0 : parseInt(e));
}

function makeBarColors(data) {
  return Array.from(data, e => e > 0 ? 'rgb(62, 117, 245)' : 'rgb(255, 99, 132)');
}

const q_labels = [
  '2 Qtrs Ago',
  '1 Qtr Ago',
  'Latest'
];

const a_labels = [
  '2 Yrs Ago',
  '1 Yr Ago',
  'Latest'
];

const q_data = {
  labels: q_labels,
  datasets: [{
    label: 'Qtly YoY EPS Growth (%)',
    backgroundColor: makeBarColors(qEpsGrowthData),
    data: makeChartData(qEpsGrowthData)
  }]
};

const a_data = {
  labels: a_labels,
  datasets: [{
    label: 'Annual EPS Growth (%)',
    backgroundColor: makeBarColors(aEpsGrowthData),
    data: makeChartData(aEpsGrowthData)
  }]
};

const q_config = {
  type: 'bar',
  data: q_data,
  options: {
    aspectRatio: 1,
    plugins: {
      legend: {
        labels: {
          boxWidth: 0,
          color: 'rgb(175, 255, 255)',
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(175, 255, 255, 0.5)'
        },
        ticks: {
          color: 'rgb(175, 255, 255)'
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(175, 255, 255, 0.5)'
        },
        ticks: {
          color: 'rgb(175, 255, 255)'
        }
      }
    }
  }
};

const a_config = {
  type: 'bar',
  data: a_data,
  options: {
    aspectRatio: 1,
    plugins: {
      legend: {
        labels: {
          boxWidth: 0,
          color: 'rgb(175, 255, 255)',
          font: {
            size: 16,
            weight: 'bold'
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(175, 255, 255, 0.5)'
        },
        ticks: {
          color: 'rgb(175, 255, 255)'
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(175, 255, 255, 0.5)'
        },
        ticks: {
          color: 'rgb(175, 255, 255)'
        }
      }
    }
  }
};

Chart.defaults.font.family = "system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue','Noto Sans','Liberation Sans',Arial,sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji'";

const qEpsGrowthChart = new Chart(
  document.getElementById('q-eps-growth-chart'),
  q_config
);

const aEpsGrowthChart = new Chart(
  document.getElementById('a-eps-growth-chart'),
  a_config
);
