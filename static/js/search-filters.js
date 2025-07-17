document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    const doctorsListContainer = document.querySelector('.doctor-search-list');

    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(filterForm);
            const queryString = new URLSearchParams(formData).toString();
            console.log('Submitting with filters:', queryString); // Add logging

            const url = `${window.location.pathname}?${queryString}`;

            // Update URL without reloading the page
            window.history.pushState({}, '', url);

            // Make AJAX request
            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                if (doctorsListContainer) {
                    doctorsListContainer.innerHTML = html;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });

        // Handle radio button changes
        const radioButtons = filterForm.querySelectorAll('input[type="radio"]');
        radioButtons.forEach(radio => {
            radio.addEventListener('change', () => {
                console.log('Radio changed:', radio.name, radio.value); // Add logging
                filterForm.dispatchEvent(new Event('submit'));
            });
        });
    }
});
