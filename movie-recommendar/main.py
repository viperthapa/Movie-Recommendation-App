import os
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends,Request,Form,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import create_db_tables
from database import engine, SessionLocal, get_db
from models import Movie
from load_data import load_csv_to_db
from recommendar import MovieRecommender

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and load initial data
    create_db_tables()
    db = SessionLocal()
    try:
        if db.query(Movie).count() == 0:
            load_csv_to_db(db)
    finally:
        db.close()
    yield

app = FastAPI(title="Movie Recommendation System", lifespan=lifespan)

# Setup templates
templates = Jinja2Templates(directory="templates")


# Get the absolute path to the static directory
static_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")



@app.get("/")
async def home(request: Request,db:Session = Depends(get_db)):
    """Page Showing movies and recommendation"""
    recommender = MovieRecommender(db)
    popular_movies = recommender.get_popular_movies()

    all_movies = db.query(Movie).order_by(Movie.id.desc()).limit(10).all()
    print("all_movies:", all_movies)

    return templates.TemplateResponse("index.html",{
        "request":request,
        "popular_movies":popular_movies,
        "all_movies":all_movies
    })


@app.get("/api/movies/{movie_id}")
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get specific movie details"""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return {
        "id": movie.id,
        "title": movie.title,
        "genre": movie.genre,
        "year": movie.year,
        "rating": movie.rating,
        "description": movie.description,
        "poster_url": movie.poster_url
    }


@app.get("/api/recommendations/{movie_id}")
async def get_recommendations(movie_id: int, db: Session = Depends(get_db)):
    """Get movie recommendations based on content similarity"""
    recommender = MovieRecommender(db)
    recommendations = recommender.get_content_based_recommendation(movie_id, 4)
    
    if not recommendations:
        raise HTTPException(status_code=404, detail="No recommendations found")
    
    return recommendations



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)