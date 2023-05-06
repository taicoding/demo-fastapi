from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movies import Movies as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

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


@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()

    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@ movie_router.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content=[], status_code=404)
    return JSONResponse(content=jsonable_encoder(result))


@ movie_router.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movie_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    db = Session()
    results = MovieService(db).get_movie_by_category(category)
    if not results:
        return JSONResponse(content=[], status_code=404)
    return JSONResponse(content=jsonable_encoder(results))


@ movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(
    movie: Movie,
) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Movie created"}, status_code=201)


@ movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:

    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "Movie updated"}, status_code=200)


@ movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movies(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    MovieService(db).delete_movies(id)
    return JSONResponse(content={"message": "Movie deleted"}, status_code=200)
