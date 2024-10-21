// JavaScript for UI Interactions and Dynamic Elements

// Toggle the visibility of elements (e.g., collapsible sections)
function toggleVisibility(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

// Event listener for navigation menu toggle on mobile devices
document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('open');
        });
    }
});

// Form validation before submission
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) {
        console.error('Form not found:', formId);
        return false;
    }
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('input-error');
            isValid = false;
        } else {
            input.classList.remove('input-error');
        }
    });
    if (!isValid) {
        alert('Please fill in all required fields.');
    }
    return isValid;
}

// Highlighting table rows on hover
document.addEventListener('DOMContentLoaded', () => {
    const tableRows = document.querySelectorAll('table tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseover', () => {
            row.classList.add('highlight');
        });
        row.addEventListener('mouseout', () => {
            row.classList.remove('highlight');
        });
    });
});

// Modal handling (e.g., for displaying model registration details)
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Utility function to fetch data from an API endpoint
async function fetchData(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('An error occurred while fetching data. Please try again later.');
    }
}

// Sample usage: Fetch and display models list
document.addEventListener('DOMContentLoaded', () => {
    const modelsListButton = document.getElementById('fetch-models');
    if (modelsListButton) {
        modelsListButton.addEventListener('click', async () => {
            const models = await fetchData('/models/list');
            if (models) {
                const modelsContainer = document.getElementById('models-container');
                modelsContainer.innerHTML = '';
                models.forEach(model => {
                    const modelDiv = document.createElement('div');
                    modelDiv.textContent = `${model.model_name} (Uploaded by: ${model.uploaded_by})`;
                    modelsContainer.appendChild(modelDiv);
                });
            }
        });
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
