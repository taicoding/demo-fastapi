from fastapi import Body, FastAPI, HTTPException, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.requests import Request
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Mi primera App con FastAPI"
app.version = "0.0.1"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(
                status_code=403, detail="Credenciales invalidas")


class User(BaseModel):
    email: str
    password: str


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


@app.post("/login", tags=["auth"], response_model=dict, status_code=200)
def login(user: User) -> dict:
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
        return JSONResponse(content={"token": token}, status_code=200)


@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200)


@ app.get(
    "/movies/{id}",
    tags=["movies"],
    response_model=Movie,
)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[], status_code=404)


@ app.get("/movies/", tags=["movies"], response_model=List[Movie])
def get_movie_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    data = [item for item in movies if item["category"] == category]
    return JSONResponse(content=data)


@ app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(
    movie: Movie,
) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "Movie created"}, status_code=201)


@ app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(content={"message": "Movie updated"}, status_code=200)


@ app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movies(id: int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Movie deleted"}, status_code=200)
