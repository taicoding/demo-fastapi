from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi primera App con FastAPI"
app.version = "0.0.1"
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
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return {"message": "No se encontro la pelicula"}


@app.get("/movies/", tags=["movies"])
def get_movie_by_category(category: str, year: int):
    return [item for item in movies if item["category"] == category]


@app.post("/movies", tags=["movies"])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body(),
):
    m = {
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category,
    }
    movies.append(m)
    return movies


@app.put("/movies/{id}", tags=["movies"])
def update_movie(
    id: int,
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body(),
):
    for item in movies:
        if item["id"] == id:
            item["title"] = title
            item["overview"] = overview
            item["year"] = year
            item["rating"] = rating
            item["category"] = category
            return movies


@app.delete("/movies/{id}", tags=["movies"])
def delete_movies(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies
