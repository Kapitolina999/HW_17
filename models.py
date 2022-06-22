from sqlalchemy.orm import relationship

from setup_db import db


class Movie(db.Model):
    """
    Модель таблицы movies
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    trailer = db.Column(db.String(250))
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    # genre = relationship('Genre')
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    # director = relationship('Director')


class Genre(db.Model):
    """
    Модель таблицы genres
    """
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    # movies = relationship('Movie')


class Director(db.Model):
    """
    Модель таблицы directors
    """
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    # movies = relationship('Movie')
