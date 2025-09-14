from pydantic import BaseModel
from datetime import datetime


# ----------------------------
# Movie Schemas
# ----------------------------
class MovieBase(BaseModel):
    title: str
    genre: str
    year: int
    rating: float
    description: str
    poster_url: str


class MovieCreate(MovieBase):
    """Schema for creating a new movie"""
    pass


class Movie(MovieBase):
    """Schema for returning movie details"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ----------------------------
# UserRating Schemas
# ----------------------------
class UserRatingBase(BaseModel):
    user_id: str
    movie_id: int
    rating: float


class UserRatingCreate(UserRatingBase):
    """Schema for creating a user rating"""
    pass


class UserRating(UserRatingBase):
    """Schema for returning user rating details"""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
