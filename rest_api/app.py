import logging.config

import os
from flask import Flask, Blueprint
from decouple import Config, RepositoryEnv

from rest_api.database import db
from rest_api.database.models import Author, Book
from rest_api.api.restplus import api
from rest_api.api.endpoints.authors import ns as author_namespace
from rest_api.api.endpoints.books import ns as book_namespace

app = Flask(__name__)
app_config_file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './app.conf'))
app_file_config = Config(RepositoryEnv(app_config_file_path))
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), './logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
DEBUG_FLAG = app_file_config.get('DEBUG', cast=bool)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = app_file_config.get('SERVER_NAME')
    flask_app.config['PROPAGATE_EXCEPTIONS'] = app_file_config.get('PROPAGATE_EXCEPTIONS')

    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = app_file_config.get('SWAGGER_UI_DOC_EXPANSION')
    flask_app.config['RESTPLUS_VALIDATE'] = app_file_config.get('RESTPLUS_VALIDATE', cast=bool)
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = app_file_config.get('RESTPLUS_MASK_SWAGGER', cast=bool)
    flask_app.config['ERROR_404_HELP'] = app_file_config.get('RESTPLUS_ERROR_404_HELP', cast=bool)

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = app_file_config.get('SQLALCHEMY_DATABASE_URI')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app_file_config.get('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    flask_app.config['SQLITE_FILE_PATH'] = flask_app.config['SQLALCHEMY_DATABASE_URI'].replace("sqlite:///", "")


def initialize_app(flask_app):
    configure_app(flask_app)
    db.init_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(author_namespace)
    api.add_namespace(book_namespace)
    flask_app.register_blueprint(blueprint)

    if not os.path.exists(flask_app.config['SQLITE_FILE_PATH']):
        with app.app_context():
            db.create_all()

            author1 = Author("Adam", "Mickiewicz")
            author2 = Author("Adam", "Mickiewicz2")
            book = Book("Dziady", "123")
            book.authors.append(author1)
            book.authors.append(author2)

            db.session.add(author1)
            db.session.add(author2)
            db.session.add(book)
            db.session.commit()


if __name__ == "__main__":
    initialize_app(app)
    app.run(debug=DEBUG_FLAG)
