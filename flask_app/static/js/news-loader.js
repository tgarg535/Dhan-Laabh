document.addEventListener('DOMContentLoaded', () => {
    const newsContainer = document.getElementById('news-container');
    const stockSymbol = window.stockSymbol;

    // Safety check: Only run if the news container and symbol exist on the page
    if (!newsContainer || !stockSymbol) {
        return;
    }

    // Function to format the date
    const formatDate = (dateString) => {
        if (!dateString) return 'Date not available';
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };
    
    // Show a loading state
    newsContainer.innerHTML = `
        <div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-8">
            <p class="text-gray-500 dark:text-gray-400">Fetching latest news...</p>
        </div>
    `;

    fetch(`/api/news/${stockSymbol}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(articles => {
            // Clear loading state
            newsContainer.innerHTML = '';

            if (!articles || articles.length === 0) {
                newsContainer.innerHTML = `
                    <div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-8">
                        <p class="text-gray-600 dark:text-gray-400">No recent news articles found for this stock.</p>
                    </div>
                `;
                return;
            }

            // --- THIS IS THE MODIFIED SECTION ---
            // Slice the array to get only the first 9 articles before looping
            articles.slice(0, 9).forEach(article => {
                // Use the correct fields from the newsdata.io API response
                const title = article.title || 'No Title Available';
                const source = article.source_id || 'Unknown Source';
                const imageUrl = article.image_url;
                const url = article.link || '#';
                const publishedAt = formatDate(article.pubDate);
                const description = article.description || 'No description available.';

                const newsCard = `
                    <a href="${url}" target="_blank" rel="noopener noreferrer" class="block bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-xl shadow-lg overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                        ${imageUrl ? `<img class="h-48 w-full object-cover" src="${imageUrl}" alt="News article image">` : ''}
                        <div class="p-6">
                            <p class="text-sm font-semibold text-cyan-600 dark:text-cyan-400 uppercase">${source}</p>
                            <h3 class="mt-2 text-lg font-bold text-gray-900 dark:text-white leading-tight">${title}</h3>
                            <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">${description.substring(0, 100)}...</p>
                            <p class="mt-4 text-xs text-gray-400 dark:text-gray-500">${publishedAt}</p>
                        </div>
                    </a>
                `;
                newsContainer.innerHTML += newsCard;
            });
        })
        .catch(error => {
            console.error('Error fetching news:', error);
            newsContainer.innerHTML = `
                <div class="col-span-1 md:col-span-2 lg:col-span-3 text-center py-8">
                    <p class="text-red-500 dark:text-red-400">Could not load news. Please try again later.</p>
                </div>
            `;
        });
});