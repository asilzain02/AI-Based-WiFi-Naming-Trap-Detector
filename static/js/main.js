document.addEventListener('DOMContentLoaded', () => {
    const loader = document.getElementById('loader');
    const scanBtn = document.getElementById('scan-btn');
    const toggleBtn = document.getElementById('toggle-view');
    const tableView = document.getElementById('table-view');
    const cardView = document.getElementById('card-view');

    // Show loader on scan button click
    scanBtn?.addEventListener('click', () => {
        loader.classList.remove('hidden');
    });

    // Toggle between table and card view
    toggleBtn?.addEventListener('click', () => {
        tableView.classList.toggle('hidden');
        cardView.classList.toggle('hidden');
    });
});
