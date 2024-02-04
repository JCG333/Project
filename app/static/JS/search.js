/* Contributors: Justin Gavrell*/

/*----- Get regions -----*/
function getRegions() {
    fetch('/regions')
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            // Create option for each region in the database
            data.regions.forEach(region => {
                var option = document.createElement('option');
                option.value = region.region;
                option.textContent = region.region;
                document.querySelector('#regions-filter').append(option);
            });
        })
        // Error handling
        .catch(error => {
            showError(error.message);
        });
}

/*----- Get parks -----*/
function getParks() {
    fetch('/parks')
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            // Create option for each park in the database
            data.parks.forEach(park => {
                var option = document.createElement('option');
                option.value = park.park;
                option.textContent = park.park;
                document.querySelector('#parks-filter').append(option);
            });
        })
        // Error handling
        .catch(error => {
            showError(error.message);
        });
}
/*----- Get turbines -----*/
function getTurbines() {
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            company: 'Company1',
            region: document.getElementById('regions-filter').value,
            park: document.getElementById('parks-filter').value
        })
    })
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            // Create table entry for each turbine in the database
            let turbines = '<table>';
            turbines += '<tr><th>ID</th><th>Turbine</th></tr>';
            data.turbines.forEach(turbine => {
                turbines += `
            <tr style="cursor: pointer;" onclick="window.location='tubrine/${turbine.id}';">
                <td>${turbine.id}</td>
                <td>${turbine.turbine}</td>
            </tr>
        `;
            });
            turbines += '</table>';
            document.getElementById('turbine-list').innerHTML = turbines;
        })
        // Error handling
        .catch(error => {
            showError(error.message);
        });
}
/*----- Search bar (key triggered)-----*/
function search_key(event) {
    if (event.key === 'Enter') {
        var searchQuery = document.getElementById('search').value;
        fetch('/search_turbine/' + searchQuery)
            // check if response is OK
            .then(response => {
                if (!response.ok) {
                    return response.json().then(error => Promise.reject(error));
                }
                return response.json();
            })
            // if OK
            .then(data => {
                // Create table entry for each turbine that matches the search query
                let turbines = '<table>';
                turbines += '<tr><th>ID</th><th>Turbine</th></tr>';
                data.turbines.forEach(turbine => {
                    turbines += `
                    <tr style="cursor: pointer;" onclick="window.location='tubrine/${turbine.id}';">
                        <td>${turbine.id}</td>
                        <td>${turbine.turbine}</td>
                    </tr>
                `;
                });
                turbines += '</table>';
                document.getElementById('turbine-list').innerHTML = turbines;
            })
            // Error handling
            .catch(error => {
                showError(error.message);
            });
    }
}
/*----- Search bar (button triggered) -----*/
function search_button() {
    var searchQuery = document.getElementById('search').value;
    fetch('/search_turbine/' + searchQuery)
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            // Create table entry for each turbine that matches the search query
            let turbines = '<table>';
            turbines += '<tr><th>ID</th><th>Turbine</th></tr>';
            data.turbines.forEach(turbine => {
                turbines += `
                    <tr style="cursor: pointer;" onclick="window.location='tubrine/${turbine.id}';">
                        <td>${turbine.id}</td>
                        <td>${turbine.turbine}</td>
                    </tr>
                `;
            });
            turbines += '</table>';
            document.getElementById('turbine-list').innerHTML = turbines;
        })
        // Error handling
        .catch(error => {
            showError(error.message);
        });
}
/*----- Event listeners for Search bar -----*/
document.getElementById('search').addEventListener('keypress', search_key);
document.getElementById('search-button').addEventListener('click', search_button);

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

/*----- option select event listener -----*/
document.getElementById('regions-filter').addEventListener('change', getTurbines);
document.getElementById('parks-filter').addEventListener('change', getTurbines);

/*----- account redirect -----*/
function account() {
    window.location = '/account';
}
document.getElementById('account-icon-button').addEventListener('click', account);

/*----- Window load -----*/
window.onload = function () {
    getRegions();
    getParks();
    getTurbines();

}