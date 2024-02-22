
document.querySelectorAll('.chart-nav-button').forEach(button => {
  button.addEventListener('click', function () {
    // Remove active class from all buttons
    document.querySelectorAll('.chart-nav-button').forEach(btn => btn.classList.remove('active'));

    // Add active class to clicked button
    this.classList.add('active');

    // Display corresponding chart

  });
});

/*----- dropdown -----*/

document.getElementById('ham-menu').addEventListener('click', function (event) {
  var dropdownContent = document.getElementById('myDropdown');
  if (dropdownContent.style.display !== "block") {
    dropdownContent.style.display = "block";
  } else {
    dropdownContent.style.display = "none";
  }
  event.stopPropagation();
});
// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function () {
  var dropdownContent = document.getElementById('myDropdown');
  dropdownContent.style.display = "none"; // Hide the dropdown when anywhere else on the window is clicked
});
// Prevent clicks inside the dropdown from closing the dropdown
document.getElementById('myDropdown').addEventListener('click', function (event) {
  event.stopPropagation(); // Stop the click event from bubbling up to parent elements
});

/*----- error message -----*/
function showError(message) {
  var errorMessage = document.getElementById('error-message');
  errorMessage.innerHTML = '<p>Error: ' + message + '</p>';
  errorMessage.style.display = 'block'; // Show the error message

  // Hide the error message after 5 seconds
  setTimeout(function () {
    errorMessage.style.display = 'none';
  }, 5000);
}

/*----- Pin turbine -----*/
function pinTurbine(turbine_id) {
  fetch('/pin_turbine/' + turbine_id)
    // check if response is OK
    .then(response => {
      if (!response.ok) {
        return response.json().then(error => Promise.reject(error));
      }
      return response.json();
    })
    // if OK
    .then(data => {
      console.log('sucessfully pinned!');
    })
    // Error handling
    .catch(error => {
      showError(error.message);
    });
}
/*----- unpin turbine ------*/
function unpinTurbine(turbine_id) {
  return fetch('/unpin_turbine/' + turbine_id)
    // check if response is OK
    .then(response => {
      if (!response.ok) {
        return response.json().then(error => Promise.reject(error));
      }
      return response.json();
    })
    // if OK
    .then(data => {
      console.log('sucessfully unpinned!');
    })
    // Error handling
    .catch(error => {
      showError(error.message);
    });
}

document.querySelectorAll('.pin-button').forEach(function (button) {
  button.addEventListener('click', function (event) {
    event.stopPropagation();
    let button = document.querySelector('.pin-button');
    let turbineId = button.dataset.turbineid;
    if (this.classList.contains('on')) {
      unpinTurbine(turbineId);
      this.textContent = 'Pin';
      this.classList.remove('on');
    } else {
      pinTurbine(turbineId);
      this.classList.add('on');
      this.textContent = 'Pinned';
    }
  });
});

/*----- Window load -----*/
window.onload = function () {

}

/*
var TurbName = "Turbine-W0XX";
var TurbPark = "ParkYY";
var TurbReg = "Norrbotten";

var latestTurbMin = 32;
var TurbTime = getCurrentTime()[0] + ":" + latestTurbMin;

function getTurbInfo() {
  document.getElementById("TurbineName").innerHTML = TurbName;
  document.getElementById("TurbinePark").innerHTML = TurbPark;
  document.getElementById("TurbineRegion").innerHTML = TurbReg;
  document.getElementById("TurbineTime").innerHTML = TurbTime;
}

function getCurrentTime() {
  var d = new Date();
  var h = d.getHours();
  var m = d.getMinutes();
  if (h < 10) { h = "0" + h; }
  if (m < 10) { m = "0" + m; }
  return [h, m];
}

function getTimeArray() {
  const timeRangeP = (start) => Array.from({ length: 13 }, (_, i) => start + i);
  const p12h = timeRangeP(new Date().getHours());
  for (var i in p12h) {
    if (p12h[i] >= 24) { p12h[i] = p12h[i] - 24; }
    if (p12h[i] < 10) { p12h[i] = "0" + p12h[i]; }
    p12h[i] = p12h[i] + ":" + TurbTime.substring(TurbTime.length - 2);;
  }

  const m12h = p12h.slice();
  p12h.reverse();
  p12h.pop();

  const timeArray = p12h.concat(m12h);

  return (timeArray);
}

const riskValues = Array.from({ length: 25 }, () => Math.floor(Math.random() * 3));

function rChart() {
  const ctx = document.getElementById('riskChart');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: getTimeArray(),
      datasets: [{
        data: riskValues,
        borderWidth: 1,
        fill: true,
      }]
    },
    options: {
      scales: {
        y: {
          position: 'left',
          beginAtZero: true,
          max: 2,
          min: 0,
          ticks: {
            stepSize: 1
          }
        },
        y1: {
          position: 'right',
          beginAtZero: true,
          max: 2,
          min: 0,
          ticks: {
            stepSize: 1
          }
        },
        x: {
          ticks: {
            maxTicksLimit: 25
          }
        }
      },
      plugins: {
        legend: {
          display: false,
        }
      }
    }
  });
}

const tempValues = Array.from({ length: 25 }, () => Math.floor(Math.random() * 60) - 30);

function tChart() {
  const ctx = document.getElementById('tempChart');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: getTimeArray(),
      datasets: [{
        data: tempValues,
        borderWidth: 1,
      }]
    },
    options: {
      scales: {
        y: {
          position: 'left',
          beginAtZero: true,
          max: 30,
          min: -30,
          ticks: {
            stepSize: 5
          }
        },
        y1: {
          position: 'right',
          beginAtZero: true,
          max: 30,
          min: -30,
          ticks: {
            stepSize: 5
          }
        },
        x: {
          ticks: {
            maxTicksLimit: 25
          }
        }
      },
      plugins: {
        legend: {
          display: false,
        }
      }
    }
  });
}

const downValues = Array.from({ length: 25 }, () => Math.floor(Math.random() * 100) / 100);

function dChart() {
  const ctx = document.getElementById('downChart');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: getTimeArray(),
      datasets: [{
        data: downValues,
        borderWidth: 1,
      }]
    },
    options: {
      scales: {
        y: {
          position: 'left',
          beginAtZero: true,
          max: 1,
          ticks: {
            stepSize: 0.1
          }
        },
        y1: {
          position: 'right',
          beginAtZero: true,
          max: 1,
          ticks: {
            stepSize: 0.1
          }
        },
        x: {
          ticks: {
            maxTicksLimit: 25
          }
        }
      },
      plugins: {
        legend: {
          display: false,
        }
      }
    }
  });
}
*/