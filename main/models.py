from sqlalchemy import Column, Integer, String, Date, Text, Index
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    date_of_release = Column(Date, default=func.now(), nullable=False)
    description = Column(Text)
    genre = Column(String(50), nullable=False)

book_genre_index = Index('book_genre_index', Book.genre)