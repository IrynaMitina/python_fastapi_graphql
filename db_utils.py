from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker


DB_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DB_URL, echo=True) 
async_session = async_sessionmaker(engine, expire_on_commit=False)