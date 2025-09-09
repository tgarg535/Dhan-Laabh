//Market Data Loader
document.addEventListener('DOMContentLoaded', function() {
    const tableBody = document.getElementById('market-snapshot-body');

    if (tableBody) {
        // Function to format large numbers (like volume)
        const formatVolume = (volume) => {
            if (volume >= 1_000_000_000) return (volume / 1_000_000_000).toFixed(2) + 'B';
            if (volume >= 1_000_000) return (volume / 1_000_000).toFixed(2) + 'M';
            if (volume >= 1_000) return (volume / 1_000).toFixed(2) + 'K';
            return volume;
        };
        
        // Show a loading state with theme-aware text color
        tableBody.innerHTML = `<tr><td colspan="7" class="text-center py-8 text-gray-500 dark:text-gray-400">Loading live market data...</td></tr>`;

        fetch('/api/market-data')
            .then(response => response.json())
            .then(data => {
                // Clear loading state
                tableBody.innerHTML = '';
                
                if (data.error) {
                     tableBody.innerHTML = `<tr><td colspan="7" class="text-center py-8 text-red-600 dark:text-red-400">Error fetching market data. Please try again later.</td></tr>`;
                     console.error("API Error:", data.error);
                     return;
                }

                data.forEach(stock => {
                    const price = stock.price.toFixed(2);
                    const change = stock.change.toFixed(2);
                    const changePercent = stock.changePercent.toFixed(2);
                    const dayHigh = stock.dayHigh.toFixed(2);
                    const dayLow = stock.dayLow.toFixed(2);
                    const volume = formatVolume(stock.volume);
                    
                    const changeColorClass = stock.change >= 0 ? 'text-green-700 dark:text-green-400' : 'text-red-600 dark:text-red-500';
                    const changeSign = stock.change >= 0 ? '+' : '';

                    const row = `
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <div class="flex-shrink-0 h-10 w-10">
                                        <img class="h-10 w-10 rounded-full object-cover" src="${stock.logo || 'https://placehold.co/40x40/e5e7eb/4b5563?text=?'}" alt="${stock.name} logo">
                                    </div>
                                    <div class="ml-4">
                                        <div class="text-sm font-medium text-gray-900 dark:text-white">${stock.name}</div>
                                        <div class="text-xs text-gray-500 dark:text-gray-400">${stock.symbol}</div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">$${price}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium ${changeColorClass}">
                                ${changeSign}${change} (${changeSign}${changePercent}%)
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">$${dayHigh}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">$${dayLow}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 dark:text-gray-300">${volume}</td>
                            <td class="px-6 py-4 whitespace-nowrap text-center">
                                <a href="${stock.website}" target="_blank" rel="noopener noreferrer" class="text-cyan-700 bg-cyan-100 hover:bg-cyan-200 dark:text-cyan-400 dark:bg-cyan-900/50 dark:hover:bg-cyan-900 text-xs font-semibold py-1 px-3 rounded-full transition-colors">
                                    Visit Site
                                </a>
                            </td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });
            })
            .catch(error => {
                tableBody.innerHTML = `<tr><td colspan="7" class="text-center py-8 text-red-600 dark:text-red-400">Could not connect to the server. Please check your connection.</td></tr>`;
                console.error('Error fetching market data:', error);
            });
    }
});