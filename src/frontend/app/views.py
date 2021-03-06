# views.py

from flask import render_template, redirect, url_for, request

from app import app
from api.biblio import Biblio

bib = Biblio()


@app.route('/')                                         # Home
def index():
    return render_template("/index.html")


@app.route('/books')                                    # Books
def books():
    return render_template("books.html")


@app.route('/profile')                                  # Profile
def profile():
    return render_template("profile.html")


@app.route('/return_book', methods=['POST', 'GET'])     # Return Book
def return_book():
    if request.method == 'POST':
        book_id = request.form["book_id"]
        result = bib.return_book(book_id)
        if result is True:
            result_text = f"Book {book_id} successfully returned."
            return render_template("success.html", return_book_result=result_text)
        else:
            result_text = f"Book {book_id} couldn't be returned."
            return render_template("fail.html", return_book_result=result_text)


@app.route('/list_read_books', methods=['POST', 'GET'])     # Reading History
def list_read_books():
    if request.method == 'POST':
        print(request.form)
        result = bib.list_read_books()
        print(result.head())
        return render_template("includes/table.html", tables=[result.to_html(classes="data")], titles=result.columns.values)


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template("app/templates/search.html")


@app.route('/active_loans', methods=['POST', 'GET'])
def active_loans():
    return render_template("table.html")


@app.route('/loan_history', methods=['POST', 'GET'])
def loan_history():
    return render_template("table.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/settings')
def settings():
    return render_template("settings.html")


###########################################################################


@app.route('/dev', methods=['POST', 'GET'])                       # Testing
def dev():
    return render_template("dev.html")
