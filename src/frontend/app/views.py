# views.py

from flask import render_template, redirect, url_for, request

from app import app
from api.biblio import Biblio

bib = Biblio()


@app.route('/')  # Home
def index():
    return render_template("/index.html")


@app.route('/books')  # Books
def books():
    return render_template("books.html")


@app.route('/profile')  # Profile
def profile():
    return render_template("profile.html")


@app.route('/return_book', methods=['POST', 'GET'])  # Return Book
def return_book():
    return render_template("return_book.html")


@app.route('/list_read_books', methods=['POST', 'GET'])  # Reading History
def list_read_books():
    result = bib.list_read_books()
    print(result)
    return render_template("includes/table.html", column_names=result.columns.values, row_data=list(result.values.tolist()),
                           title='Reading History', sub_header='Already read')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template("app/templates/search.html")


@app.route('/active_loans', methods=['POST', 'GET'])
def active_loans():
    return render_template("loans_active.html")


@app.route('/loan_history', methods=['POST', 'GET'])
def loan_history():
    return render_template("loans_history.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/settings')
def settings():
    return render_template("settings.html")


###########################################################################


@app.route('/dev', methods=['POST', 'GET'])  # Testing
def dev():
    return render_template("_dev.html")
