document.addEventListener('DOMContentLoaded', function() {
    // Initialize masonry layout only if grid exists
    const grid = document.querySelector('.image-grid');
    if (grid) {
        const masonry = new Masonry(grid, {
            itemSelector: '.grid-item',
            columnWidth: '.grid-sizer',
            percentPosition: true,
            gutter: 10
        });

        // Initialize lazy loading
        const lazyLoadInstance = new LazyLoad({
            elements_selector: ".lazy",
            callback_loaded: (el) => {
                masonry.layout();
            }
        });

        // Search functionality
        const searchInput = document.getElementById('search');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(function(e) {
                const searchTerm = e.target.value.toLowerCase();
                const items = document.querySelectorAll('.grid-item');
                
                items.forEach(item => {
                    const tags = item.dataset.tags?.toLowerCase() || '';
                    const description = item.dataset.description?.toLowerCase() || '';
                    
                    if (tags.includes(searchTerm) || description.includes(searchTerm)) {
                        item.style.display = '';
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                masonry.layout();
            }, 300));
        }
    } else {
        // Initialize lazy loading for other layouts
        const lazyLoadInstance = new LazyLoad({
            elements_selector: ".lazy"
        });
    }
});

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
