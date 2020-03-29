import logging
import traceback

from flask import request
from flask_restplus import Resource
from datetime import date

from sqlalchemy.orm.exc import NoResultFound

from rest_api.api.serializers import book, book_with_authors
from rest_api.api.restplus import api
from rest_api.database.models import Book, Author, db

log = logging.getLogger(__name__)

ns = api.namespace('books', description='Operations related to books')


@ns.route('/')
class BooksCollection(Resource):

    @api.marshal_list_with(book)
    def get(self):
        """
        Returns list of books.
        """
        books = Book.query.all()
        return books

    @api.expect(book)
    def post(self):
        """
        Creates a new book.
        """
        data = request.json

        book_id = data.get('id')
        title = data.get('title')
        isbn = data.get('isbn')
        pub_date = date.fromtimestamp(data.get("pub_date_timestamp"))

        author_id = data.get('author_id')
        author_obj = Author.query.filter(Author.id == author_id).one()

        book_obj = Book(title, isbn, [author_obj], pub_date)
        book_obj.authors.append(author_obj)
        if book_id:
            book_obj.id = author_id

        db.session.add(book_obj)
        db.session.commit()
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Book not found.')
class PostItem(Resource):

    @api.marshal_with(book_with_authors)
    def get(self, id):
        """
        Returns a book with authors.
        """
        try:
            book_obj = Book.query.filter(Book.id == id).one()
        except NoResultFound as e:
            log.error(traceback.format_exc())
            return {'message': 'A database result was required but none was found.'}, 404
        except Exception as e:
            message = 'An unhandled exception occurred: ' + str(e)
            log.error(message)
            return {'message': message}, 500

        return book_obj

    @api.expect(book)
    @api.response(204, 'Book successfully updated.')
    def put(self, id):
        """
        Updates a book.
        """
        data = request.json
        try:
            book_obj = Book.query.filter(Book.id == id).one()
            book_obj.title = data.get('title')
            book_obj.isbn = data.get('isbn')
            book_obj.pub_date = date.fromtimestamp(data.get("pub_date_timestamp"))

            author_id = data.get('author_id')
            author_obj = Author.query.filter(Author.id == author_id).one()
            book_obj.authors.append(author_obj)

            db.session.add(book_obj)
            db.session.commit()
        except NoResultFound as e:
            log.error(traceback.format_exc())
            return {'message': 'A database result was required but none was found.'}, 404
        except Exception as e:
            message = 'An unhandled exception occurred: ' + str(e)
            log.error(message)
            return {'message': message}, 500

        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, id):
        """
        Deletes book.
        """
        try:
            book_obj = Book.query.filter(Book.id == id).one()
            db.session.delete(book_obj)
            db.session.commit()
        except NoResultFound as e:
            log.error(traceback.format_exc())
            return {'message': 'A database result was required but none was found.'}, 404
        except Exception as e:
            message = 'An unhandled exception occurred: ' + str(e)
            log.error(message)
            return {'message': message}, 500
        return None, 204
