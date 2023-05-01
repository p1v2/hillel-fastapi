import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]


async def get_session():
    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
    )
    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return session
