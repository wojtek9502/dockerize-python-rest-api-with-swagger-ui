import logging

from flask_restplus import Api


log = logging.getLogger(__name__)

api = Api(version='1.0', title='Library API')