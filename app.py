from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

from db_utils import DB
from graphql_types import Query, Mutation

app = FastAPI()


@app.on_event("startup")
async def startup():
    await DB.connect()  # init connection pool


@app.on_event("shutdown")
async def shutdown():
    await DB.disconnect()  # close all db connections


schema = strawberry.Schema(query=Query, mutation=Mutation)
app.include_router(GraphQLRouter(schema, graphiql=False), prefix="/graphql")
app.include_router(GraphQLRouter(schema, graphiql=True), prefix="/graphiql")
