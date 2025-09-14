import os
import csv
from sqlalchemy.orm import Session
from models import Movie
CSV_FILE = os.path.join(os.path.dirname(__file__), "movie_dataset.csv")

def load_csv_to_db(db: Session):
    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        movies = [
            Movie(
                title=row["title"],
                genre=row["genre"],
                year=int(row["year"]),
                rating=float(row["rating"]),
                description=row["description"],
                poster_url=row["poster_url"],
            )
            for row in reader
        ]
        db.bulk_save_objects(movies)
        db.commit()