# Movie Recommendation System

A FastAPI-based movie recommendation system that provides personalized movie recommendations using content-based filtering techniques with TF-IDF (Term Frequency – Inverse Document Frequency) algorithm.

## Features

- Content-based movie recommendations
- Popular movies listing
- Interactive web interface
- RESTful API endpoints
- Responsive design

## Tech Stack

- FastAPI
- SQLAlchemy
- Jinja2 Templates
- scikit-learn
- pandas
- SQLite

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd movie-recommendation-ap
```

2. Create a virtual environment
```bash
python -m venv <your_env_name>
source your_env_name/bin/activate  # On Windows use: your_env_name\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Start the FastAPI server:
```bash
cd movie-recommendar
uvicorn main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## API Endpoints

- `GET /`: Main web interface
- `GET /api/movies/{movie_id}`: Get specific movie details
- `GET /api/recommendations/{movie_id}`: Get movie recommendations

## Project Structure

```
movie-recommendar/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   └── index.html
├── main.py
├── models.py
├── database.py
├── recommendar.py
└── load_data.py
```

## Development

The project uses:
- FastAPI for the web framework
- SQLAlchemy for database operations
- scikit-learn for recommendation algorithms
- Jinja2 for templating
- Custom CSS and JavaScript for the frontend

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Snapshot

![Movie Recommendation System](docs/images/snapshot.png)

*Movie Recommendation System Interface*

## License

This project is licensed under the MIT License - see the LICENSE file for details