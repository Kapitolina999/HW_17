import data
from models import Movie, Genre, Director, db
from app import create_app

app = create_app()
app.app_context().push()

# Удаление и создание таблиц
db.drop_all()
db.create_all()

# Создание объектов для добавления в БД
genres = [Genre(id=_['pk'], name=_['name']) for _ in data.genres]
directors = [Director(id=_['pk'], name=_['name']) for _ in data.directors]
movies = [Movie(id=_['pk'],
                title=_['title'],
                year=_['year'],
                description=_['description'],
                trailer=_['trailer'],
                rating=_['rating'],
                genre_id=_['genre_id'],
                director_id=_['director_id']) for _ in data.movies]


# Добавление объектов в таблицы
db.session.add_all(genres)
db.session.add_all(directors)
db.session.add_all(movies)
db.session.commit()
