document.addEventListener('DOMContentLoaded', function () {
    // Toggle function for dropdowns
    function toggleDropdown(id) {
        const dropdown = document.getElementById(id);
        if (dropdown) {
            dropdown.classList.toggle('show');
        }
    }

    // Assign listeners to each section explicitly
    const servicesImage = document.querySelector('[data-toggle="services"]');
    if (servicesImage) {
        servicesImage.addEventListener('click', function () {
            toggleDropdown('services-dropdown');
        });
    }

    const staffImage = document.querySelector('[data-toggle="staff"]');
    if (staffImage) {
        staffImage.addEventListener('click', function () {
            toggleDropdown('staff-dropdown');
        });
    }
});