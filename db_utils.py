import databases
import sqlalchemy


DATABASE_URL = "sqlite:///./test.db"
DB = databases.Database(DATABASE_URL)


metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
PERSONS_TABLE = sqlalchemy.Table(
    "persons", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    autoload=True, autoload_with=engine
)

MOVIES_TABLE = sqlalchemy.Table(
    "movies", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    autoload=True, autoload_with=engine
)

ACTORS_TABLE = sqlalchemy.Table(
    "actors", metadata, autoload=True, autoload_with=engine
)