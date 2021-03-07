from flask import render_template, request, session
from flask_login import login_required, current_user
from pandas import DataFrame

from api.selections import Selections
from api.biblio import Biblio
from api.book import Book
from app import app

bib = Biblio()
app.secret_key = 'dljsawadslqk24e21cjn!Ew@@dsa5'


@app.context_processor
def logged_in():
    return dict(is_logged_in=session.get('is_logged_in', None),
                user=session.get('user_name', None),
                user_id=session.get('user_id', None))


@app.route('/')  # Home
def index():
    return render_template("/index.html", user=session.get('user_name'))


@app.route('/book')
def book():
    result = bib.get_select("SELECT * FROM book_extended")
    print(request)
    print(result)
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Books', sub_header='List of all your books', link_column='none',
                               zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='Site could not be loaded.')


@app.route('/loan_or_read_book', methods=['POST', 'GET'])
def loan_or_read_book():
    if request.method == 'POST':
        id = request.form['book_id']
        if request.form['do'] == 'Loan':
            result = bib.make_loan(int(request.form['book_id']))
        if request.form['do'] == 'Read':
            result = bib.mark_book_as_read(int(request.form['book_id']))
            print(f"Book read: {result}")
        if result is True:
            return render_template("includes/success.html", title='Success',
                                   text='Action executed successfully.')
    return render_template("includes/fail.html", title='Error',
                           text='Something went wrong.')


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    return render_template("add_book.html")


@app.route('/execute_add_book', methods=['POST', 'GET'])
def execute_add_book():
    new_book = Book()
    new_book.set_via_isbn(request.form['book_isbn'])
    result = bib.add_new_book(new_book)
    if result is True:
        return render_template("includes/success.html", title='New book added',
                               text='You have add a new book successfully.')
    return render_template("includes/fail.html", title='No book added',
                           text='You have not added the book.')


@app.route('/execute_add_book_manually', methods=['POST', 'GET'])
def execute_add_book_manually():
    new_book = Book()
    edition = request.form['book_edition']
    if edition == "":
        edition = 1
    param_list = [request.form['author_first_names'],
                  request.form['author_first_names'],
                  request.form['publisher_name'],
                  request.form['book_title'],
                  edition,
                  request.form['book_language'],
                  request.form['book_genre'],
                  request.form['book_isbn'],
                  request.form['publishing_year'],
                  request.form['location_id'],
                  request.form['reco_age']]
    final_list = list()
    for param in param_list:
        if param == "":
            param = None
        final_list.append(param)
    new_book.set_manually(final_list)
    result = bib.add_new_book(new_book)
    if result is True:
        return render_template("includes/success.html", title='New book added',
                               text='You have add a new book successfully.')
    return render_template("includes/fail.html", title='No book added',
                           text='You have not added the book.')


@app.route('/profile')  # Profile
def profile():
    return render_template("profile.html")


@app.route('/return_book', methods=['POST', 'GET'])
def return_book():
    return render_template("return_book.html")


@app.route('/return_book_by_isbn', methods=['POST', 'GET'])
def return_book_by_isbn():
    if request.method == 'POST':
        book_id = bib.get_book_id_by_isbn(request.form["book_isbn"])
        result = bib.return_book(book_id)
        if result is True:
            return render_template("includes/success.html", title='Book Returned',
                                   text='You have returned the book successfully.')
        return render_template("includes/fail.html", title='Book not Returned',
                               text='You have not returned the book.')


@app.route('/return_book_by_title', methods=['POST', 'GET'])
def return_book_by_title():
    if request.method == 'POST':
        edition = request.form['book_edition']
        if edition == "":
            edition = 1
        book_id = bib.get_book_id_by_title_edition(request.form["book_title"], edition)
        result = bib.return_book(book_id)
        if result is True:
            return render_template("includes/success.html", title='Book Returned',
                                   text='You have returned the book successfully.')
        return render_template("includes/fail.html", title='Book not Returned',
                               text='You have not returned the book.')


@app.route('/list_read_books', methods=['POST', 'GET'])  # Reading History
# @login_required
def list_read_books():
    result = bib.get_select(Selections.sql_read_books(session.get('user_id', None)))
    print(request)
    print(result)
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Reading History', sub_header='Already read', link_column='none', zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='Site could not be loaded.')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")
    # return render_template("includes/success.html", title='Successful Log-In',
    #                        text='You have been successfully logged in.')
    # return render_template("includes/fail.html", title='Failed Log-In',
    #                        text='You have not been logged in.')


@app.route('/logged_in', methods=['POST', 'GET'])
def logged_in():
    session['user_id'] = bib.set_user(request.form['user_name'], request.form['password'])
    if session.get('user_id') is False:
        return render_template("includes/fail.html", title='Failed Log-In',
                               text='You have not been logged in.')
    session['is_logged_in'] = 'logged_in'
    session['user_name'] = request.form['user_name']
    print(session.get('user_id', None))
    return render_template("includes/success.html", title='Successful Login',
                           text='You have been successfully logged in.')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['is_logged_in'] = 'logged_out'
    session['user_name'] = 'no name'
    session['user_id'] = None
    bib.s_user = None
    return render_template("includes/success.html", title='Successful Logout',
                           text='You have been successfully logged out.')
    # return render_template("includes/fail.html", title='Failed Log-In',
    #                        text='You have not been logged in.')


@app.route('/search', methods=['POST', 'GET'])
def search():
    return render_template("app/templates/search.html")


@app.route('/active_loans', methods=['POST', 'GET'])
def active_loans():
    result = bib.get_select(Selections.sql_user_active_loans(session.get('user_id', None)))
    print(request)
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Loans', sub_header='List of all your active loans', link_column='none',
                               zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='Site could not be loaded.')


@app.route('/loan_history', methods=['POST', 'GET'])
def loan_history():
    result = bib.get_select(Selections.sql_user_loan_history(session.get('user_id', None)))
    print(request)
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Loans', sub_header='List of all your past loans', link_column='none',
                               zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='Site could not be loaded.')


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
