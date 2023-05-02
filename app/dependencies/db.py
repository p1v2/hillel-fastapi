import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]


async def get_session():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True,
    )
    SessionMaker = sessionmaker(engine, expire_on_commit=False, class_=Session)
    return SessionMaker()
