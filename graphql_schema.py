from typing import List, Optional
import strawberry
from strawberry.types import Info
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import selectinload

from db_models import MovieModel
from db_utils import async_session
from graphql_utils import get_field_names

def any_item_starts_with(prefix, items):
    return any(map(lambda x: x.startswith(prefix), items))


@strawberry.type
class Person():
    id: int
    full_name: str
    birth_date: str
    type: str  # TODO: enum['actor', 'director']

    @classmethod
    def factory(cls, person):
        kwargs = {k:v for k,v in person.__dict__.items() if not k.startswith("_")}
        person_t = cls(**kwargs)
        return person_t


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
    def factory(cls, movie):
        kwargs = {k:v for k,v in movie.__dict__.items() if not k.startswith("_")}
        director = Person.factory(movie.director) if 'director' in kwargs else None
        actors = [Person.factory(item) for item in movie.actors] if 'actors' in kwargs else None
        kwargs['director'] = director
        kwargs['actors'] = actors
        movie_t = cls(**kwargs)
        return movie_t


@strawberry.input
class InputFilter():
    country: Optional[str] = None
    release_year: Optional[str] = None


async def _resolve_movies(root:Movie, info:Info, **kwargs) -> List[Movie]:
    requested_field_names = get_field_names(info)
    # if director object was requested
    stmt = select(MovieModel)
    if any_item_starts_with(".movies.director.", requested_field_names):
        stmt = stmt.options(selectinload(MovieModel.director))
    if any_item_starts_with(".movies.actors.", requested_field_names):
        stmt = stmt.options(selectinload(MovieModel.actors))
        
    if kwargs['filter']:
        if kwargs['filter'].country:
            stmt = stmt.where(MovieModel.country==kwargs['filter'].country)
        if kwargs['filter'].release_year:
            stmt = stmt.where(MovieModel.release_year==kwargs['filter'].release_year)
    print(stmt)
    async with async_session() as session:
        res = await session.scalars(stmt)
    items = res.all()
    movies = [Movie.factory(item) for item in items]
    return movies
    

async def add_movie(self, title: str, release_year: str, 
                    director_id: int, genres: str, country: str='USA') -> Movie:
    movie = MovieModel(
        title=title, release_year=release_year, country=country,
        director_id=director_id, genres=genres
    )
    async with async_session() as session:
        session.add(movie)
        await session.commit()

    return Movie.factory(movie)


@strawberry.type
class Query:
    @strawberry.field
    def movies(self, info:Info, filter: Optional[InputFilter]=None) -> List[Movie]:
        return _resolve_movies(self, info, filter=filter)


@strawberry.type
class Mutation:
    add_movie: Movie = strawberry.mutation(resolver=add_movie)
