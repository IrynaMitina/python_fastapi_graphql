from typing import List, Optional
import strawberry
from strawberry.types import Info
from sqlalchemy.sql.expression import join, select

from db_utils import DB, MOVIES_TABLE, PERSONS_TABLE, ACTORS_TABLE
from graphql_utils import get_field_names


@strawberry.type
class Person():
    id: int
    full_name: str
    birth_date: str
    type: str  # TODO: enum['actor', 'director']

    @classmethod
    def factory(cls, item_dict):
        prefix = "persons_"
        person_kwargs = {k[len(prefix):]:v for k,v in item_dict.items() if k.startswith(prefix)}
        person = None if not person_kwargs else cls(**person_kwargs)
        return person


@strawberry.type
class Movie():
    id: int
    title: str
    release_year: str
    country: str
    director: Person
    director_id: int
    genres: str
    actors: List[Person]

    @classmethod
    def factory(cls, item_dict):
        prefix = "movies_"
        director = Person.factory(item_dict)
        movie_kwargs = {k[len(prefix):]:v for k,v in item_dict.items() if k.startswith(prefix)}
        movie_kwargs['director'] = director
        movie_kwargs['actors'] = None
        return cls(**movie_kwargs)


@strawberry.input
class InputFilter():
    country: Optional[str] = None
    release_year: Optional[str] = None


async def _resolve_movies(root:Movie, info:Info, **kwargs) -> List[Movie]:
    # ? Person.__dataclass_fields__.keys()
    requested_field_names = get_field_names(info)
    # if director object was requested
    if any([fieldname.startswith(".movies.director.") for fieldname in requested_field_names]):
        query = select([MOVIES_TABLE, PERSONS_TABLE], use_labels=True) \
            .select_from(MOVIES_TABLE.join(
                PERSONS_TABLE, 
                MOVIES_TABLE.c.director_id==PERSONS_TABLE.c.id
            ))
    else:
        query = select([MOVIES_TABLE], use_labels=True)
    if kwargs['filter']:
        if kwargs['filter'].country:
            query = query.where(MOVIES_TABLE.c.country==kwargs['filter'].country)
        if kwargs['filter'].release_year:
            query = query.where(MOVIES_TABLE.c.release_year==kwargs['filter'].release_year)
    print(query)
    column_names = query.columns.keys()
    rows = await DB.fetch_all(query)  # movies
    rows = [dict(zip(column_names, row)) for row in rows]

    movies = [Movie.factory(row) for row in rows]

    if any([fieldname.startswith(".movies.actors.") for fieldname in requested_field_names]):
        movie_ids = [row["movies_id"] for row in rows]
        query = select([ACTORS_TABLE, PERSONS_TABLE], use_labels=True) \
            .select_from(ACTORS_TABLE.join(
                PERSONS_TABLE, 
                ACTORS_TABLE.c.person_id==PERSONS_TABLE.c.id
            )).where(ACTORS_TABLE.c.movie_id.in_(movie_ids))
        print(query)  
        column_names = query.columns.keys()
        rows = await DB.fetch_all(query)  # actors
        rows = [dict(zip(column_names, row)) for row in rows]
        actors_map = {}
        for row in rows:
            actors_map.setdefault(row["actors_movie_id"], []).append(row)
        for movie in movies:
            movie.actors = [Person.factory(row) for row in actors_map[movie.id]]

    return movies


async def add_movie(self, title: str, description: str, premiere_date: str = '2000-01-01') -> int:
    new_movie_dict = {
        "title": title, "description": description, 
        "premiere_date": premiere_date
    }
    query = MOVIES_TABLE.insert().values(**new_movie_dict)
    last_record_id = await DB.execute(query)
    new_movie_dict["id"] = last_record_id
    return Movie(**new_movie_dict)


@strawberry.type
class Query:
    @strawberry.field
    def movies(self, info:Info, filter: Optional[InputFilter]=None) -> List[Movie]:
        return _resolve_movies(self, info, filter=filter)


@strawberry.type
class Mutation:
    add_movie: Movie = strawberry.mutation(resolver=add_movie)
