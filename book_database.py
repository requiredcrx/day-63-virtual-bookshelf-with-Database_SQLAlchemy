from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from main import BookShelf, EditForm


"""
This has been deprecated and re written inside the main.py
"""

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db.init_app(app)


class BookStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True, nullable=False)
    author = db.Column(db.String(60), nullable=False)
    rating = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

with app.app_context():
    shelf = BookShelf()
    new_book = BookStore(title=shelf.book_name.data, author=shelf.author_name.data, rating=shelf.rating.data)
    db.session.add(new_book)
    db.session.commit()

