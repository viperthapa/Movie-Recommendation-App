import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from models import Movie
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:

    def __init__(self,db:Session):
        self.db = db
        self.movies_df = None
        self.cosine_sim = None
        self.load_data()

    def load_data(self):
        movie_data = []
        movies = self.db.query(Movie).all()

        movie_data = []
        for movie in movies:
            movie_data.append({
                'id':movie.id,
                'title': movie.title,
                'genre': movie.genre,
                'year': movie.year,
                'rating': movie.rating,
                'description': movie.description,
                'poster_url': movie.poster_url,
                'content': f"{movie.genre} {movie.description}"  # Combine for similarity
            })
        
        self.movies_df = pd.DataFrame(movie_data)
        
        if not self.movies_df.empty:
            # Create TF-IDF matrix for content-based filtering
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(self.movies_df['content'].fillna(''))
            
            # Compute cosine similarity matrix
            self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


    def get_content_based_recommendation(self, movie_id: int, num_recommendations: int = 5):
        if self.movies_df is None or self.movies_df.empty:
            return []
        
        try:
            # Get the index of the movie
            idx = self.movies_df[self.movies_df['id'] == movie_id].index[0]
            
            # Get similarity scores for all movies
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            
            # Sort movies based on similarity scores
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Get indices of most similar movies (excluding the input movie)
            movie_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]
            
            # Return recommended movies
            recommended_movies = []
            for idx in movie_indices:
                movie_data = self.movies_df.iloc[idx]
                recommended_movies.append({
                    'id': int(movie_data['id']),
                    'title': movie_data['title'],
                    'genre': movie_data['genre'],
                    'year': int(movie_data['year']),
                    'rating': float(movie_data['rating']),
                    'poster_url': movie_data['poster_url']
                })
            
            return recommended_movies
        except IndexError:
            return []
        
    def get_popular_movies(self, num_movies: int = 8):
        """Get popular movies based on ratings"""
        if self.movies_df is None or self.movies_df.empty:
            return []
        
        # Sort by rating and return top movies
        top_movies = self.movies_df.nlargest(num_movies, 'rating')
        
        popular_movies = []
        for _, movie in top_movies.iterrows():
            popular_movies.append({
                'id': int(movie['id']),
                'title': movie['title'],
                'genre': movie['genre'],
                'year': int(movie['year']),
                'rating': float(movie['rating']),
                'poster_url': movie['poster_url']
            })
        
        return popular_movies

        