from marshmallow import Schema, fields


# Создаем схемы для конвертации данных
class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    year = fields.Int()
    description = fields.Str()
    trailer = fields.Str()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)