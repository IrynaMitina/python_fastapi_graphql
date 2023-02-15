from typing import List
from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
import sqlalchemy
import databases


DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
movies_table = sqlalchemy.Table(
    "movies", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    autoload=True, autoload_with=engine
)

@strawberry.type
class Movie():
    id: int
    title: str
    description: str
    premiere_date: str


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def resolve_movies(self) -> List[Movie]:
    query = movies_table.select()
    items = await database.fetch_all(query)
    return [Movie(**item) for item in items]

async def add_movie(self, title: str, description: str, premiere_date: str = '2000-01-01') -> int:
    new_movie_dict = {
        "title": title, "description": description, 
        "premiere_date": premiere_date
    }
    query = movies_table.insert().values(**new_movie_dict)
    last_record_id = await database.execute(query)
    new_movie_dict["id"] = last_record_id
    return Movie(**new_movie_dict)

@strawberry.type
class Query:
    movies: List[Movie] = strawberry.field(resolver=resolve_movies)

@strawberry.type
class Mutation:
    add_movie: Movie = strawberry.mutation(resolver=add_movie)

schema = strawberry.Schema(query=Query, mutation=Mutation)
app.include_router(GraphQLRouter(schema, graphiql=False), prefix="/graphql")
app.include_router(GraphQLRouter(schema, graphiql=True), prefix="/graphiql")

