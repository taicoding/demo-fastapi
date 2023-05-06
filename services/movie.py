from models.movies import Movies as MovieModel
from schemas.movie import Movie


class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result

    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).filter(
            MovieModel.category == category).all()
        return result

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return True

    def update_movie(self, id, movie: Movie):
        u_movie = self.db.query(MovieModel).filter(
            MovieModel.id == id).first()
        u_movie.title = movie.title
        u_movie.overview = movie.overview
        u_movie.year = movie.year
        u_movie.category = movie.category
        self.db.commit()
        return True

    def delete_movie(self, id):
        d_movie = self.db.query(MovieModel).filter(
            MovieModel.id == id).delete()
        self.db.commit()
        return True
