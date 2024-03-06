function changeLanguage(lang) {
    $.post("/change_language", {lang: lang}, function(data) {
        if (data.status == 'success') {
            alert(data.message);
            location.reload();  // Reload the page to update the language
        }
    });
}


// Changes the theme of the website when pressing the theme buttons
function changeTheme(theme) {
    // Send a POST request to the server to update the theme
    $.post("/change_theme", {theme: theme}, function(data) {
        if (data.status == 'success') {
            // If the update was successful, change the theme on the client side
            var element = document.body;
            element.classList.remove('light-mode', 'dark-mode'); // Remove both classes
            element.classList.add(theme + '-mode'); // Add the new theme class
            location.reload();  // Reload the page to update the theme
        }
    });
}



window.onload = function() {
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
}