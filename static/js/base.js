const sidebar = document.querySelector(".sidebar");
const sidebarToggler = document.querySelector('.sidebar-toggler');

// Toggler sidebar's collapsed state
sidebarToggler.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
});