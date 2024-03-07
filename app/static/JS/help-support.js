document.addEventListener('DOMContentLoaded', function () {
    // Hide all content sections except the placeholder section
    const contentSections = document.querySelectorAll('.content-section');
    contentSections.forEach(section => {
        section.style.display = 'none';
    });

    // Show the placeholder section
    const placeholderSection = document.getElementById('placeholder-section');
    if (placeholderSection) {
        placeholderSection.style.display = 'block';
    }
});

function toggleSection(sectionId) {
    // Hide all content sections
    const contentSections = document.querySelectorAll('.content-section');
    contentSections.forEach(section => {
        section.style.display = 'none';
    });

    // Show the selected content section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}
