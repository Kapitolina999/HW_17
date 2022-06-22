import json
from flask import Flask, request, jsonify
from flask_restx import Api, Resource

from models import Movie, Genre, Director
from setup_db import db
from schemas import movie_schema, movies_schema
from schemas import genre_schema, genres_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}


def create_app():
    db.init_app(app)
    return app


app = create_app()

api = Api(app)
movie_ns = api.namespace('movies')
genre_ns = api.namespace('genres')
director_ns = api.namespace('directors')


@movie_ns.route("/")
class MoviesView(Resource):

    def get(self):
        did = request.args.get('director_id')
        gid = request.args.get('genre_id')

        if did and gid is None:
            all_movies = db.session.query(Movie.title).filter(Movie.director_id == did).all()
        elif gid and did is None:
            all_movies = db.session.query(Movie.title).filter(Movie.genre_id == gid).all()
        elif gid and did:
            all_movies = db.session.query(Movie.title).filter(Movie.genre_id == gid, Movie.director_id == did).all()
        else:
            all_movies = db.session.query(Movie.title).all()

        return jsonify(movies_schema.dump(all_movies))

    def post(self):
        data_json = json.loads(request.data)
        movie_new = Movie(**data_json)
        # movie_new = movie_schema.load(data_json)
        db.session.add(movie_new)
        db.session.commit()
        return f"Фильм '{movie_new.title}' добавлен", 201


@movie_ns.route("/<int:mid>")
class MovieView(Resource):

    def get(self, mid):
        movie = db.session.query(Movie).get(mid)
        return jsonify(movie_schema.dump(movie))

    def put(self, mid):
        movie = db.session.query(Movie).get(mid)
        data_movie = request.json
        movie.title = data_movie['title']
        movie.description = data_movie['description']
        movie.trailer = data_movie['trailer']
        movie.rating = data_movie['rating']
        movie.year = data_movie['year']
        movie.genre_id = data_movie['genre_id']
        movie.director_id = data_movie['director_id']
        db.session.add(movie)
        db.session.commit()
        return f"Данные фильма id{movie.id} обновлены", 200

    def patch(self, mid):
        movie = db.session.query(Movie).get(mid)
        data_movie = request.json
        attributes = [key for key in data_movie.keys()]

        if 'title' in attributes:
            movie.title = data_movie['title']
        if 'year' in attributes:
            movie.year = data_movie['year']
        if 'description' in attributes:
            movie.description = data_movie['description']
        if 'trailer' in attributes:
            movie.trailer = data_movie['trailer']
        if 'rating' in attributes:
            movie.rating = data_movie['rating']
        if 'genre_id' in attributes:
            movie.genre_id = data_movie['genre_id']
        if 'director_id' in attributes:
            movie.director_id = data_movie['director_id']

        db.session.add(movie)
        db.session.commit()
        return f'Внесены изменения в фильм id {movie.id}', 200

    def delete(self, mid):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return "Фильм удален", 200


@genre_ns.route('/')
class GenresView(Resource):

    def get(self):
        all_genres = db.session.query(Genre).all()
        return jsonify(genres_schema.dump(all_genres)), 200

    def post(self):
        data_genre = request.json
        new_genre = Genre(id=data_genre['id'], name=data_genre['name'])
        db.session.add(new_genre)
        db.session.commit()
        return f"Жанр {new_genre.name} добавлен"


@genre_ns.route('/<int:gid>')
class GenreView(Resource):

    def get(self, gid):
        genre = db.session.query(Genre).get(gid)
        return jsonify(genre_schema.dump(genre))

    def put(self, gid):
        genre = db.session.query(Genre).get(gid)
        data_genre = request.json
        genre.id = data_genre['id']
        genre.name = data_genre['name']
        db.session.add(genre)
        db.session.commit()
        return f"Данные жанра {genre.name} обновлены", 200


if __name__ == '__main__':
    app.run(debug=False)


