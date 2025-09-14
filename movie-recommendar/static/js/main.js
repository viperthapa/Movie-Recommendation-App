
function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alertContainer');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    alertContainer.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}


async function getRecommendations(movieId = null) {
    const selectedMovieId = movieId || document.getElementById('movieSelect').value;
    
    if (!selectedMovieId) {
        showAlert('Please select a movie first!', 'error');
        return;
    }

    const recommendationsSection = document.getElementById('recommendationsSection');
    const recommendationsGrid = document.getElementById('recommendationsGrid');
    
    recommendationsSection.style.display = 'block';
    recommendationsGrid.innerHTML = '<div class="loading">Finding similar movies...</div>';

    try {
        const response = await fetch(`/api/recommendations/${selectedMovieId}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch recommendations');
        }

        const recommendations = await response.json();
        
        if (recommendations.length === 0) {
            recommendationsGrid.innerHTML = '<div class="alert alert-info">No similar movies found.</div>';
            return;
        }

        recommendationsGrid.innerHTML = recommendations.map(movie => `
            <div class="movie-card" onclick="getRecommendations(${movie.id})">
                <div class="movie-poster">
                    <img src="${'/static/images/thumbnail.jpg'}" 
                         alt="${movie.title}"
                         onerror="handleImageError(this)">
                    <div class="movie-rating">⭐ ${movie.rating.toFixed(1)}</div>
                </div>
                <div class="movie-info">
                    <div class="movie-title">${movie.title}</div>
                    <div class="movie-genre">${movie.genre}</div>
                    <div class="movie-year">${movie.year}</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error:', error);
        recommendationsGrid.innerHTML = '<div class="alert alert-error">Failed to load recommendations. Please try again.</div>';
    }
}

// Initialize if needed
document.addEventListener('DOMContentLoaded', function() {
    // Any initialization code can go here
});