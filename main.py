from fastapi import Body, FastAPI, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()
app.title = "Mi primera App con FastAPI"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    year: int = Field(gt=2000, lt=2024)
    rating: float = Field(gt=0, le=10)
    category: str = Field(max_length=15, min_length=5)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Avatar",
                "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
                "year": "2009",
                "rating": 7.8,
                "category": "Acción",
            }
        }


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción",
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Drama",
    },
]


@app.get("/", tags=["home"])
def message():
    return HTMLResponse("<h1> Hola esto es un endpoint</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["movies"])
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return item
    return {"message": "No se encontro la pelicula"}


@app.get("/movies/", tags=["movies"])
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)):
    return [item for item in movies if item["category"] == category]


@app.post("/movies", tags=["movies"])
def create_movie(
    movie: Movie,
):
    movies.append(movie)
    return movies


@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return movies


@app.delete("/movies/{id}", tags=["movies"])
def delete_movies(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies
