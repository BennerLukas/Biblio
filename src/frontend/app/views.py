from flask import render_template, request, session
from pandas import DataFrame

from api.selections import Selections
from app import app
from api.biblio import Biblio

bib = Biblio()
app.secret_key = 'dljsawadslqk24e21cjn!Ew@@dsa5'


@app.context_processor
def logged_in():
    return dict(is_logged_in=session.get('is_logged_in', None),
                user=session.get('user_name', None),
                user_id=session.get('user_id', None))


@app.route('/')  # Home
def index():
    session['is_logged_in'] = 'logged_out'
    session['user_name'] = 'no name'
    session['user_id'] = None

    return render_template("/index.html")


@app.route('/book')  # Books
def book():
    result = bib.get_select("SELECT * FROM book_extended")
    print(request)
    print(result)
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Books', sub_header='List of all your books', link_column='b_is_available',
                               zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='Site could not be loaded.')


@app.route('/add_book', methods=['POST', 'GET'])  # Return Book
def add_book():
    return render_template("add_book.html")


@app.route('/profile')  # Profile
def profile():
    return render_template("profile.html")


@app.route('/return_book', methods=['POST', 'GET'])  # Return Book
def return_book():
    return render_template("return_book.html")


@app.route('/list_read_books', methods=['POST', 'GET'])  # Reading History
def list_read_books():
    result = bib.list_read_books()
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
    session['is_logged_in'] = 'logged_in'
    session['user_name'] = 'fritz'
    session['user_id'] = 1
    return render_template("login.html")
    # return render_template("includes/success.html", title='Successful Log-In',
    #                        text='You have been successfully logged in.')
    # return render_template("includes/fail.html", title='Failed Log-In',
    #                        text='You have not been logged in.')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['is_logged_in'] = 'logged_out'
    session['user_name'] = 'no name'
    session['user_id'] = None
    return render_template("logout.html")
    # return render_template("includes/success.html", title='Successful Log-In',
    #                        text='You have been successfully logged in.')
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
                               title='Books', sub_header='List of all your books', link_column='b_is_available',
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
                               title='Books', sub_header='List of all your books', link_column='b_is_available',
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
