# views.py

from flask import render_template, redirect, url_for, request

from app import app
from api.biblio import Biblio

bib = Biblio()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/list_read_books', methods=['POST', 'GET'])
def list_read_books():
    if request.method == 'POST':
        print(request.form)
        result = bib.list_read_books()
        print(result.head())
        return render_template("table.html", tables=[result.to_html(classes="data")], titles=result.columns.values)


@app.route('/return_book', methods=['POST', 'GET'])
def return_book():
    if request.method == 'POST':
        book_id = request.form["book_id"]
        result = bib.return_book(book_id)
        print(result)
        return render_template("index.html", return_book_result=result)
