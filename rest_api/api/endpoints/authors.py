import logging
import traceback

from flask import request
from flask_restplus import Resource
from rest_api.api.serializers import author, author_with_books
from rest_api.api.restplus import api
from rest_api.database.models import Author
from rest_api.database import db
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

ns = api.namespace('authors', description='Operations related to authors')


@ns.route('/')
class AuthorCollection(Resource):

    @api.marshal_list_with(author)
    def get(self):
        """
        Returns list of authors.
        """
        categories = Author.query.all()
        return categories

    @api.response(201, 'Author successfully created.')
    @api.expect(author)
    def post(self):
        """
        Creates a new blog category.
        """
        data = request.json

        name = data.get('name')
        surname = data.get('surname')
        author_id = data.get('id')

        author = Author(name, surname)
        if author_id:
            author.id = author_id

        db.session.add(author)
        db.session.commit()
        return str(author), 201


@ns.route('/<int:id>')
@api.response(404, 'Author not found.')
class AuthorItem(Resource):

    @api.marshal_with(author_with_books)
    def get(self, id):
        """
        Returns a author with a list of books.
        """
        try:
            authors = Author.query.filter(Author.id == id).one()
        except NoResultFound as e:
            log.error(traceback.format_exc())
            return {'message': 'A database result was required but none was found.'}, 404
        except Exception as e:
            message = 'An unhandled exception occurred: ' + str(e)
            log.error(message)
            return {'message': message}, 500

        return authors

    @api.expect(author)
    @api.response(204, 'Author successfully updated.')
    def put(self, id):
        """
        Updates a Author.

        Use this method to change the name and surname of a author.

        * Send a JSON object with the new name in the request body.

        ```
        {
          "id": 1,
          "name": "new_name",
          "surname": "new_surname",
        }
        ```

        * Specify the ID of the author to modify in the request URL path.
        """
        data = request.json

        try:
            author_obj = Author.query.filter(Author.id == id).one()
            author_obj.name = data.get('name')
            author_obj.name = data.get('surname')
            db.session.add(author_obj)
            db.session.commit()
        except NoResultFound as e:
            log.error(traceback.format_exc())
            return {'message': 'A database result was required but none was found.'}, 404
        except Exception as e:
            message = 'An unhandled exception occurred: ' + str(e)
            log.error(message)
            return {'message': message}, 500

        return None, 204

    @api.response(204, 'Author successfully deleted.')
    def delete(self, id):
        """
        Deletes author.
        """
        try:
            author_obj = Author.query.filter(Author.id == id).one()
            db.session.delete(author_obj)
            db.session.commit()
        except NoResultFound as e:
            log.error(traceback.format_exc())
            return {'message': 'A database result was required but none was found.'}, 404
        except Exception as e:
            message = 'An unhandled exception occurred: ' + str(e)
            log.error(message)
            return {'message': message}, 500

        return None, 204
