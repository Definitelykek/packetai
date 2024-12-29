import os
from venv import create

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv
from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from datetime import datetime

load_dotenv()

engine = create_async_engine(url=os.getenv("DB_URL"))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Request(Base):
    __tablename__ = "requests"
    id :Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    text :Mapped[str] = mapped_column(String(1000))
    answer :Mapped[str] = mapped_column(String(1000))
    date :Mapped[datetime] = mapped_column(DateTime, default=datetime.now())


class User(Base):
    __tablename__ = "users"
    id :Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    model = mapped_column(String, default="gpt-4o")

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)