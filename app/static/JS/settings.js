function changeLanguage(lang) {
    $.post("/change_language", {lang: lang}, function(data) {
        if (data.status == 'success') {
            alert(data.message);
            location.reload();  // Reload the page to update the language
        }
    });
}