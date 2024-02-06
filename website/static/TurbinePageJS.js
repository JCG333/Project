var TurbName = "Turbine-W0XX";
var TurbPark = "ParkYY";
var TurbReg = "Norrbotten";

var latestTurbMin = 32;
var TurbTime = getCurrentTime()[0] +":"+ latestTurbMin;

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
  if (h<10) {h = "0"+h;}
  if (m<10) {m = "0"+m;}
  return [h, m];
}

function getTimeArray(){
  const timeRangeP = (start) => Array.from({ length: 13 }, (_, i) => start + i);
  const p12h = timeRangeP(new Date().getHours());
  for (var i in p12h) {
    if (p12h[i]>=24){p12h[i]=p12h[i]-24;}
    if (p12h[i]<10){p12h[i]="0"+p12h[i];}
    p12h[i]=p12h[i]+":"+ TurbTime.substring(TurbTime.length - 2);;
  }

  const m12h = p12h.slice();
  p12h.reverse();
  p12h.pop();

  const timeArray = p12h.concat(m12h);

  return(timeArray);
}

const riskValues = Array.from({length: 25}, () => Math.floor(Math.random() * 3));

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

const tempValues = Array.from({length: 25}, () => Math.floor(Math.random() * 60)-30);

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

const downValues = Array.from({length: 25}, () => Math.floor(Math.random() * 100)/100);

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