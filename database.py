# import sqlite3
#
# db = sqlite3.connect('book-collection.db')
# cursor = db.cursor()
# # cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO bookS VALUES(1, 'Harry Porter', 'J. K. Rowling', '9.3')")
# db.commit()


"""
This is a test/example for database creation with flask_SQLAlchemy...
all codes beloware not part of this.... just for practice purpose
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()

# CRUD OPERATIONS
# C - CREATE
with app.app_context():
    book1 = Books(title='Brain Dead', author='J.P. Morgan', rating=9.2)
    book2 = Books(title="The Rules of Life", author="Richard Templar", rating=8.9)
    book3 = Books(title="Everything XD", author='O.O. Isaiah', rating='9.1')
    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.commit()

# R - READ, Read all records
with app.app_context():
    result = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = result.scalars()

# R - READ, Read A Particular Record By Query
with app.app_context():
    book = db.session.execute(db.select(Books).where(Books.title == "Brain Dead"))
    book_to_read = book.scalar()

# U - UPDATE, Updating A Particular Record By Query
with app.app_context():
    book_to_update = db.session.execute(db.select(Books).where(Books.title == "Everything XD")).scalar()
    book_to_update.title = "Everything YOYO"
    db.session.commit()

# Update A Record By PRIMARY KEY
book_id_1 = 1
with app.app_context():
    book_to_update = db.session.execute(db.select(Books).where(Books.id == book_id_1)).scalar()
    # or book_to_update = db.get_or_404(Book, book_id)
    book_to_update.title = "Brain Dead"
    db.session.commit()

# D - DELETE, Delete A Session By Primary Key
book_id = 2
with app.app_context():
    book_to_delete = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    # or book_to_delete = db.get_or_404(Books, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
