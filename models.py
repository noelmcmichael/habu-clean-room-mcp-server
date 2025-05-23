import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Joke(Base):
    __tablename__ = "jokes"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True)
    joke_text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
