from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter

from db_utils import engine as db_engine
from graphql_schema import Query, Mutation

app = FastAPI()


@app.on_event("shutdown")
async def shutdown():
    await db_engine.dispose() 


schema = strawberry.Schema(query=Query, mutation=Mutation)
app.include_router(GraphQLRouter(schema, graphiql=False), prefix="/graphql")
app.include_router(GraphQLRouter(schema, graphiql=True), prefix="/graphiql")
