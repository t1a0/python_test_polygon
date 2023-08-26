import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Book

@pytest.fixture
def session():
    engine = create_engine('postgresql://postgres:admin@localhost/ls_16')
    Session = sessionmaker(bind=engine)
    session = Session()
    Book.metadata.create_all(engine)
    yield session
    session.close()
    Book.metadata.drop_all(engine)

def test_create_and_read_book(session):
    book = Book(name='Sample Book', author='Sample Author', genre='Fiction')
    session.add(book)
    session.commit()

    fetched_book = session.query(Book).filter_by(name='Sample Book').first()
    assert fetched_book is not None
    assert fetched_book.author == 'Sample Author'
    assert fetched_book.genre == 'Fiction'
