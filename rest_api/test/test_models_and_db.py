import pytest

from rest_api.database.models import Author, Book
from sqlalchemy.exc import IntegrityError

authors_test_data = [
    (["Stanisław", "Lem"], ["Stanisław", "Lem"]),
    (["Adam", "BardzoDługieNazwisko"*200], ["Adam", "BardzoDługieNazwisko"*200]),
    (["BardzoDługieImie"*200, "Nazwisko"], ["BardzoDługieImie"*200, "Nazwisko"]),
]


@pytest.mark.parametrize('author_data, expected_author_data', authors_test_data)
def test_create_author_object_from_model(author_data, expected_author_data):
    name = author_data[0]
    surname = author_data[1]
    author = Author(name=name, surname=surname)

    assert [author.name, author.surname] == expected_author_data


@pytest.mark.parametrize('author_data, expected_author_data', authors_test_data)
def test_add_author_obj_to_db(init_new_db_for_every_test, author_data, expected_author_data):
    db = init_new_db_for_every_test
    name = author_data[0]
    surname = author_data[1]
    author = Author(name=name, surname=surname)

    db.session.add(author)
    db.session.commit()
    db_obj = Author.query.filter_by(name=expected_author_data[0], surname=expected_author_data[1]).first()

    assert [db_obj.name, db_obj.surname] == expected_author_data


def test_create_book_obj_for_model():
    author_obj = Author("Stanisław", "Lem")
    book_obj = Book("Bajki robotów", 1111, "1585478251")
    book_obj.authors.append(author_obj)
    expected_isbn = 1111

    assert book_obj.isbn == expected_isbn


def test_create_book_obj_with_two_autors_for_model():
    author_obj = Author("Stanisław", "Lem")
    author_obj2 = Author("Stanisław2", "Lem2")
    book_obj = Book("Bajki robotów", 1111, "1585478251")

    book_obj.authors.append(author_obj)
    book_obj.authors.append(author_obj2)
    expected_autors = [author_obj, author_obj2]

    assert book_obj.authors == expected_autors


def test_add_book_obj_to_db(init_new_db_for_every_test):
    db = init_new_db_for_every_test
    isbn = "1111"
    author_obj = Author("Stanisław", "Lem")
    book_obj = Book("Bajki robotów", isbn, "1585478251")
    book_obj.authors.append(author_obj)

    db.session.add(book_obj)
    db.session.commit()
    db_obj = Book.query.filter_by(isbn=isbn).first()

    assert db_obj.isbn == isbn


def test_add_books_with_the_same_isbn_to_db(init_new_db_for_every_test):
    db = init_new_db_for_every_test
    isbn = "1111"
    author_obj = Author("Stanisław", "Lem")
    book_obj = Book("Bajki robotów", isbn, "1585478251")
    book_obj.authors.append(author_obj)

    book_obj2 = Book("Kongres futurologiczny", isbn, "1585478251")
    book_obj2.authors.append(author_obj)

    with pytest.raises(IntegrityError):
        db.session.add(book_obj)
        db.session.add(book_obj2)
        db.session.commit()
