// Import stock symbols from the dedicated data file
import { stockSymbols } from './stock-data.js';

document.addEventListener('DOMContentLoaded', function() {

    // --- THEME TOGGLE SCRIPT ---
    const themeToggleButton = document.getElementById('theme-toggle');
    if (themeToggleButton) {
        const darkIcon = document.getElementById('theme-toggle-dark-icon');
        const lightIcon = document.getElementById('theme-toggle-light-icon');

        const applyTheme = () => {
            if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                lightIcon.classList.add('hidden');
                darkIcon.classList.remove('hidden');
                document.documentElement.classList.add('dark');
            } else {
                darkIcon.classList.add('hidden');
                lightIcon.classList.remove('hidden');
                document.documentElement.classList.remove('dark');
            }
        };

        applyTheme();

        themeToggleButton.addEventListener('click', function() {
            darkIcon.classList.toggle('hidden');
            lightIcon.classList.toggle('hidden');
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('color-theme', isDark ? 'dark' : 'light');
        });
    }

    // --- AUTOCOMPLETE & VALIDATION SCRIPT ---
    const stockForm = document.getElementById('stock-search-form');
    if (stockForm) {
        const stockInput = document.getElementById('stock_symbol');
        const resultsContainer = document.getElementById('autocomplete-results');
        const validationAlert = document.getElementById('validation-alert');

        // Client-side validation before submitting
        stockForm.addEventListener('submit', function(e) {
            const inputValue = stockInput.value.toUpperCase();
            const isValid = stockSymbols.some(stock => stock.symbol.toUpperCase() === inputValue);
            
            if (!isValid) {
                e.preventDefault(); // Stop the form submission
                validationAlert.classList.add('show');
                setTimeout(() => {
                    validationAlert.classList.remove('show');
                }, 3000);
            }
        });

        // Autocomplete functionality
        stockInput.addEventListener('input', function() {
            const value = this.value;
            closeAllLists();
            if (!value) return;

            const suggestions = document.createElement('div');
            suggestions.setAttribute('id', 'autocomplete-list');
            suggestions.setAttribute('class', 'autocomplete-items');
            resultsContainer.appendChild(suggestions);

            const filteredStocks = stockSymbols.filter(stock => 
                stock.symbol.toUpperCase().startsWith(value.toUpperCase()) || 
                stock.name.toUpperCase().includes(value.toUpperCase())
            ).slice(0, 8); // Limit to top 8

            filteredStocks.forEach(stock => {
                const item = document.createElement('div');
                item.classList.add('autocomplete-item');
                // Highlight the matching part of the symbol/name
                const symbolMatch = stock.symbol.substring(0, value.length);
                const symbolName = stock.symbol.substring(value.length);
                
                item.innerHTML = `
                    <div class="autocomplete-name">${stock.name}</div>
                    <div class="autocomplete-symbol"><strong>${symbolMatch}</strong>${symbolName}</div>
                `;
                
                item.addEventListener('click', function() {
                    stockInput.value = stock.symbol;
                    closeAllLists();
                });
                suggestions.appendChild(item);
            });
        });

        const closeAllLists = () => {
            const items = document.getElementById('autocomplete-list');
            if (items) items.remove();
        };

        document.addEventListener('click', (e) => {
            if (e.target !== stockInput) {
                closeAllLists();
            }
        });
    }
});