from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movies import Movies as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer

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


@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()

    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@ movie_router.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content=[], status_code=404)
    return JSONResponse(content=jsonable_encoder(result))


@ movie_router.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movie_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    db = Session()
    results = db.query(MovieModel).filter(
        MovieModel.category == category).all()
    if not results:
        return JSONResponse(content=[], status_code=404)
    return JSONResponse(content=jsonable_encoder(results))


@ movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(
    movie: Movie,
) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()

    return JSONResponse(content={"message": "Movie created"}, status_code=201)


@ movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:

    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(content={"message": "Movie updated"}, status_code=200)


@ movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movies(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Movie deleted"}, status_code=200)
