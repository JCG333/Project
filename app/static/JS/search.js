/* Contributors: Justin Gavrell Fredrik Larsson*/

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
            turbines += '<tr><th>ID</th><th>Turbine</th><th>Location</th><th></th></tr>';
            data.turbines.forEach(turbineData => {
                let turbine = turbineData.turbine;
                let isPinned = turbineData.pinned;
                let park = turbineData.park;
                let region = turbineData.region;
                turbines += `
                    <tr class="turbine-list-div" style="cursor: pointer;" onclick="window.location='turbine/${turbine.id}';">
                        <td class="turbine-id"><strong>${turbine.id}</strong></td>
                        <td class="turbine-name">${turbine.turbine}</td>
                        <td class="turbine-location"><i class="fas fa-map-marker-alt"></i> ${park}, ${region}</td>
                        <td class="turbine-pin"><button class="pinned-button ${isPinned ? 'on' : ''}">${isPinned ? 'Pinned' : 'Pin'}</button></td>
                    </tr>
                `;
            });
            // onclick=pinTurbine(${turbine.id})
            turbines += '</table>';
            document.getElementById('turbine-list').innerHTML = turbines;

            document.querySelectorAll('.pinned-button').forEach(function (button) {
                button.addEventListener('click', function (event) {
                    event.stopPropagation();
                    if (this.classList.contains('on')) {
                        unpinTurbine(this.parentElement.parentElement.querySelector('.turbine-id').textContent);
                        this.textContent = 'Pin';
                        this.classList.remove('on');
                    } else {
                        pinTurbine(this.parentElement.parentElement.querySelector('.turbine-id').textContent);
                        this.classList.add('on');
                        this.textContent = 'Pinned';
                    }
                });
            });
        })
        // Error handling
        .catch(error => {
            showError(error.message);
        });
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
            getPinnedTurbines();
        })
        // Error handling
        .catch(error => {
            showError(error.message);
        });
}
/*----- unpin turbine ------*/
function unpinTurbine(turbine_id) {
    fetch('/unpin_turbine/' + turbine_id)
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            getPinnedTurbines();
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
        if (searchQuery === '') {
            getTurbines();
        } else {
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
                    turbines += '<tr><th>ID</th><th>Turbine</th><th>Location</th><th></th></tr>';
                    data.turbines.forEach(turbineData => {
                        let turbine = turbineData.turbine;
                        let isPinned = turbineData.pinned;
                        let park = turbineData.park;
                        let region = turbineData.region;
                        turbines += `
                            <tr class="turbine-list-div" style="cursor: pointer;" onclick="window.location='turbine/${turbine.id}';">
                                <td class="turbine-id"><strong>${turbine.id}</strong></td>
                                <td class="turbine-name">${turbine.turbine}</td>
                                <td class="turbine-location"><i class="fas fa-map-marker-alt"></i> ${park}, ${region}</td>
                                <td class="turbine-pin"><button class="pinned-button ${isPinned ? 'on' : ''}">${isPinned ? 'Pinned' : 'Pin'}</button></td>
                            </tr>
                        `;
                    });
                    turbines += '</table>';
                    document.getElementById('turbine-list').innerHTML = turbines;

                    document.querySelectorAll('.pinned-button').forEach(function (button) {
                        button.addEventListener('click', function (event) {
                            event.stopPropagation();
                            if (this.classList.contains('on')) {
                                unpinTurbine(this.parentElement.parentElement.querySelector('.turbine-id').textContent);
                                this.textContent = 'Pin';
                                this.classList.remove('on');
                            } else {
                                pinTurbine(this.parentElement.parentElement.querySelector('.turbine-id').textContent);
                                this.classList.add('on');
                                this.textContent = 'Pinned';
                            }
                        });
                    });
                })
                // Error handling
                .catch(error => {
                    showError(error.message);
                });
        }
    }
}
/*----- Search bar (button triggered) -----*/
function search_button() {
    var searchQuery = document.getElementById('search').value;
    if (searchQuery === '') {
        getTurbines();
    } else {
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
                turbines += '<tr><th>ID</th><th>Turbine</th><th>Location</th><th></th></tr>';
                data.turbines.forEach(turbineData => {
                    let turbine = turbineData.turbine;
                    let isPinned = turbineData.pinned;
                    let park = turbineData.park;
                    let region = turbineData.region;
                    turbines += `
                        <tr class="turbine-list-div" style="cursor: pointer;" onclick="window.location='turbine/${turbine.id}';">
                            <td class="turbine-id"><strong>${turbine.id}</strong></td>
                            <td class="turbine-name">${turbine.turbine}</td>
                            <td class="turbine-location"><i class="fas fa-map-marker-alt"></i> ${park}, ${region}</td>
                            <td class="turbine-pin"><button class="pinned-button ${isPinned ? 'on' : ''}">${isPinned ? 'Pinned' : 'Pin'}</button></td>
                        </tr>
                    `;
                });
                turbines += '</table>';
                document.getElementById('turbine-list').innerHTML = turbines;

                document.querySelectorAll('.pinned-button').forEach(function (button) {
                    button.addEventListener('click', function (event) {
                        event.stopPropagation();
                        if (this.classList.contains('on')) {
                            unpinTurbine(this.parentElement.parentElement.querySelector('.turbine-id').textContent);
                            this.classList.remove('on');
                            this.textContent = 'Pin';
                        } else {
                            pinTurbine(this.parentElement.parentElement.querySelector('.turbine-id').textContent);
                            this.classList.add('on');
                            this.textContent = 'Pinned';
                        }
                    });
                });
            })
            // Error handling
            .catch(error => {
                showError(error.message);
            });
    }
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

/*------ get pinned turbines -------*/
function getPinnedTurbines() {
    fetch('/get_pinned')
        // check if response is OK
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => Promise.reject(error));
            }
            return response.json();
        })
        // if OK
        .then(data => {
            // Create div for each turbine that matches the search query
            if (data.empty) {
                document.getElementById('pinned-container').innerHTML = '<p>No pinned turbines</p>';
            } else {
                let pinned_turbines = '';
                data.pinned_turbines.forEach(turbine => {
                    pinned_turbines += `
                <div class="turbine-div" style="cursor: pointer;" onclick="window.location='turbine/${turbine.turbine_id}';">
                    <p><strong>${turbine.turbine_id}</strong></p>
                    <p>${turbine.name}</p>
                </div>
                `;
                });
                document.getElementById('pinned-container').innerHTML = pinned_turbines;
            }
        })
        // Error handling
        .catch(error => {
            showError(error.message);
        });
}

/*----- Window load -----*/
window.onload = function () {
    getRegions();
    getParks();
    getTurbines();
    getPinnedTurbines();

}