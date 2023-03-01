from sqlalchemy import Column, Table, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class PersonModel(Base): 
    __tablename__ = "persons"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    full_name = Column("full_name", String)
    birth_date = Column("birth_date", String)
    type = Column("type", String)

association_table = Table(
    "actors", Base.metadata,
    Column("person_id", ForeignKey("persons.id")),
    Column("movie_id", ForeignKey("movies.id")),
)

class MovieModel(Base): 
    __tablename__ = "movies"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    director_id = Column("director_id", Integer, ForeignKey("persons.id"))
    title = Column("title", String)
    country = Column("country", String)
    release_year = Column("release_year", String)
    genres = Column("genres", String)
    director = relationship("PersonModel")
    actors = relationship("PersonModel", uselist=True, secondary=association_table)

