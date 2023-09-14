import os

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()
# creating flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# creating instance for Bootstrap
Bootstrap5(app)

# Initializing SQLAlchemy Database
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db.init_app(app)


# creating SQLAlchemy Database Models
class BookStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True, nullable=False)
    author = db.Column(db.String(60), nullable=False)
    rating = db.Column(db.Float, nullable=False)


# creating the model above
with app.app_context():
    db.create_all()


# building forms for user to add books, author and rating from flask form
class BookShelf(FlaskForm):
    book_name = StringField('Book Name')
    author_name = StringField("Author Name")
    rating = StringField('Ratings')
    submit = SubmitField("Add")


# from flask form, creating a form to edit ratings
class EditForm(BookShelf):
    edit = StringField(render_kw={'placeholder': 'New Rating'})
    edit_button = SubmitField('Edit Rating')


# app routes for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    books = BookStore.query.all()
    return render_template('index.html', books=books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = BookShelf()
    # check if the forms are submitted
    if form.validate_on_submit():
        # check if no datas arec entered. if no, yes, then do nothing
        if not form.book_name.data.strip() and not form.author_name.data.strip() and form.rating.data == "No Rating":
            pass
        else:
            # create a database for records of the form inputs
            with app.app_context():
                new_book = BookStore(title=form.book_name.data, author=form.author_name.data, rating=form.rating.data)
                db.session.add(new_book)
                db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html', form=form)


#  editing records of the rating from the database
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book_id = BookStore.query.get(book_id)
    form = EditForm()
    if form.validate_on_submit():
        with app.app_context():
            book_to_update = db.session.execute(db.select(BookStore).where(BookStore.id == book_id)).scalar()
            book_to_update.rating = form.rating.data
            db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', form=form, book_id=book_id)


# route to delete a particular record
@app.route('/delete')
def delete():
    book = BookStore.query.get('id')
    delete_book = db.get_or_404(BookStore, book)
    db.session.delete(delete_book)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

