# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from rest_api.database import db

book_author_table = db.Table('book_author',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    isbn = db.Column(db.String(80), unique=True)
    pub_date = db.Column(db.Integer)
    authors = db.relationship('Author', backref=db.backref('books', lazy='dynamic'), secondary=book_author_table)

    def __init__(self, title, isbn, pub_date=None):
        self.title = title
        self.isbn = isbn
        if pub_date is None:
            pub_date = 0
        self.pub_date = pub_date

    def __repr__(self):
        authors_str = ""
        for author in self.authors:
            authors_str += author.surname + " " + author.name[0] + ". "
        return f'Book: {self.title} {authors_str} {self.isbn} pub_date: {self.pub_date}'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def __repr__(self):
        return f'Author: {self.name} {self.surname}'
