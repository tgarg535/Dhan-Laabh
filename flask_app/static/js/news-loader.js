document.addEventListener('DOMContentLoaded', () => {
    const newsContainer = document.getElementById('news-container');
    const stockSymbol = window.stockSymbol;

    // Safety Check: Only run if the news container and symbol exist
    if (!newsContainer || !stockSymbol) {
        return; 
    }

    // Function to format the date
    const formatDate = (dateString) => {
        if (!dateString) return 'No date available';
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        try {
            return new Date(dateString).toLocaleDateString(undefined, options);
        } catch (e) {
            return dateString; // Fallback to original string if date is invalid
        }
    };

    // Show a loading state
    newsContainer.innerHTML = '<p class="col-span-full text-center text-gray-500 dark:text-gray-400">Loading latest news...</p>';

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

            if (articles.error || !Array.isArray(articles) || articles.length === 0) {
                newsContainer.innerHTML = `<p class="col-span-full text-center text-gray-500 dark:text-gray-400">No recent news found for ${stockSymbol}.</p>`;
                console.error("API Error or no articles:", articles.error || "Empty article array returned");
                return;
            }

            // Take only the first 6 articles
            articles.slice(0, 6).forEach(article => {
                const articleCard = `
                    <a href="${article.url}" target="_blank" rel="noopener noreferrer" class="block bg-white dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden group">
                        <div class="h-40 bg-gray-200 dark:bg-gray-700">
                           <img src="${article.urlToImage || 'https://placehold.co/600x400/e5e7eb/4b5563?text=News'}" alt="Article Image" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
                        </div>
                        <div class="p-5">
                            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">${article.source.name || 'Unknown Source'} &bull; ${formatDate(article.publishedAt)}</p>
                            <h3 class="text-md font-bold text-gray-900 dark:text-white mb-2 group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">${article.title || 'No title available'}</h3>
                            <p class="text-sm text-gray-600 dark:text-gray-300 line-clamp-3">${article.description || 'No description available.'}</p>
                        </div>
                    </a>
                `;
                newsContainer.innerHTML += articleCard;
            });
        })
        .catch(error => {
            newsContainer.innerHTML = `<p class="col-span-full text-center text-red-500 dark:text-red-400">Failed to load news. Please try again later.</p>`;
            console.error('Error fetching news:', error);
        });
});

