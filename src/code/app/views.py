from flask import render_template, request, session
from pandas import DataFrame
import psycopg2

from app.selections import Selections
from app.biblio import Biblio
from app.book import Book
from app import app

bib = Biblio()
app.secret_key = 'dljsawadslqk24e21cjn!Ew@@dsa5'


@app.context_processor
def logging_in():
    return dict(is_logged_in=session.get('is_logged_in', None),
                user=session.get('user_name', None),
                user_id=session.get('user_id', None))


@app.route('/')  # Home
def index():
    # fetch amount of books currently overdue
    count_overdue_books = bib.get_select(bib.Selections.sql_exceeded_loans(info=True)).iat[0, 0]
    count_loaned_books = bib.get_select("""SELECT COUNT(DISTINCT (n_borrow_item_id)) AS Amount
                                               FROM borrow_item AS bi
                                                    LEFT JOIN loan AS l ON bi.n_loan_id = l.n_loan_id
                                               WHERE bi.b_active = 'TRUE'""").iat[0, 0]
    count_total_books = bib.get_select("SELECT COUNT(DISTINCT(n_book_id)) FROM books").iat[0, 0]

    return render_template("/index.html", amount_overdue=count_overdue_books, amount_book_total=count_total_books,
                           amount_books_loaned=count_loaned_books)
    # return render_template("/index.html", user=session.get('user_name'))


@app.route('/search', methods=['POST', 'GET'])
def search():
    text = request.form['search_text']
    result = bib.get_select(f"SELECT * FROM book_extended WHERE s_title LIKE '%{text}%'")
    if isinstance(result, DataFrame):
        return render_template("includes/table.html", column_names=result.columns.values,
                               row_data=list(result.values.tolist()),
                               title='Search', sub_header='Your search result', link_column='none',
                               zip=zip)
    else:
        return render_template("includes/fail.html", title='Error',
                               text='No book found.')


@app.route('/book')
def book():
    result = bib.get_select("SELECT * FROM book_extended")
    result = result.drop_duplicates(subset=["n_book_id"], keep='last')  # better visualisation
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
        if request.form['do'] == 'Loan':
            result = bib.make_loan(int(request.form['book_id']))
        if request.form['do'] == 'Read':
            result = bib.mark_book_as_read(int(request.form['book_id']))
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
                  request.form['author_last_names'],
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
    active_user_id = session.get('user_id', None)
    if active_user_id is not None:
        count_read_books = bib.get_select(bib.Selections.sql_total_loans_user(active_user_id)).iat[0, 0]

        user_info = bib.get_select(bib.Selections.sql_basic_user_information(active_user_id))
        user_info_names = ["First Name", "Last Name", "Date of Birth", "City", "Country of Residency"]

        # select favorite Genre + Publisher + Author
        favorites = bib.get_select(
            Selections.sql_most_loaned_books_per_genre_publisher_author_for_user(user_id=active_user_id))

        # combine names of author and drop unnecessary columns
        favorites["Favorite Author"] = favorites["Favorite Author FN"] + " " + favorites["Favorite Author LN"]
        favorites.drop(['Favorite Author FN', 'Favorite Author LN', 'count_borrowed_items'], axis=1, inplace=True)
        favorites.columns = ["Favorite Genre", "Favorite Publisher", "Favorite Author"]

        row_data_fav = list(["None" if x is None else x for x in favorites.values.tolist()[0]])
        return render_template("profile.html", read_books_count=count_read_books, user_info=user_info,
                               column_names=user_info_names,
                               row_data=list(user_info.values.tolist()), zip=zip,
                               column_names_fav=list(favorites.columns.values),
                               row_data_fav=row_data_fav, zip2=zip,
                               user=session.get('user_name', None))
    else:
        return render_template("includes/fail.html", title='Error',
                               text='You are not logged in!')


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


########################################################################################################################
# Update / Delete Pages

@app.route('/update_book', methods=['POST', 'GET'])
def update_book():
    df_book = bib.get_select("SELECT * FROM books ORDER BY n_book_id ASC")
    return render_template("update_book.html",
                           column_names=df_book.columns.values, row_data=list(df_book.values.tolist()), zip=zip)


@app.route('/execute_change_book_manually', methods=['POST', 'GET'])
def execute_change_book_manually():
    new_book = Book()

    # Determine book_id for future operations
    # if Edition is not known it will default to 1
    book_edition = request.form['book_edition']
    if book_edition == "":
        book_edition = 1

    # fetch title to use for checks
    book_title = request.form['book_title']

    # check how to determine the book_id
    # cannot determine which book if title is not present
    if book_title == "":
        return render_template("includes/fail.html", title='Transaction failed',
                               text='Transaction failed! Reason: Missing book identifier.')
    elif book_title != "":
        try:
            book_id = bib.get_select(f"""SELECT n_book_id FROM books 
                                         WHERE s_title = '{book_title}'  AND n_book_edition = {book_edition}""").iat[
                0, 0]
        except IndexError:
            return render_template("includes/fail.html", title="Transaction failed",
                                   text=f"Transaction failed! Reason: Book cannot be found or does it not exist?")

    # Operation defined by radio button in form
    if request.form['operator'] == "delete":

        try:
            bib.exec_statement(f"""DELETE FROM books WHERE n_book_id = {book_id};""")
        except psycopg2.errors.ForeignKeyViolation:
            return render_template("includes/fail.html", title='Book deletion failed',
                                   text='Delete failed! Reason: Book id cannot be deleted because of table constraints.')
        except psycopg2.errors.InFailedSqlTransaction:
            return render_template("includes/fail.html", title='Book deletion failed',
                                   text='Delete failed! Reason: Book does not exist.')
        except Exception as err:
            return render_template("includes/fail.html", title="Book deletion failed",
                                   text=f"Delete failed! Reason {err}")
        else:
            return render_template("includes/success.html", title='Book deleted',
                                   text='Book was successfully deleted.')
    else:
        param_list = [
            book_edition,
            request.form['book_language'],
            request.form['book_genre'],
            request.form['publishing_year'],
            request.form['location_id'],
            request.form['reco_age'],
            request.form['book_isbn'],
            book_title]

        result = list()
        for item in param_list:
            if item == "":
                result.append(None)
            else:
                result.append(item)

        result = bib.exec_statement(f'''UPDATE books
                                        SET (n_book_edition, s_genre, n_publishing_year,
                                            s_book_language, n_recommended_age, n_location_id, s_isbn) =
                                            ({result[0]}, '{result[2]}', {result[3]},
                                             '{result[1]}', {result[5]}, {result[4]}, {result[6]})
                                        WHERE n_book_id = {book_id};'''.replace("'None'", "NULL").replace("None",
                                                                                                          "NULL"))

        if result is True:
            return render_template("includes/success.html", title='Book updated',
                                   text='Book updated successfully')
            return render_template("includes/fail.html", title='Book update failed',
                                   text='You have not updated the book.')


@app.route('/update_author', methods=['POST', 'GET'])
def update_author():
    df_authors = bib.get_select("""SELECT n_author_id   as "Author ID",
                                          s_first_name  as "Author's first name",
                                          s_last_name   as "Author's last name",
                                          n_address_id   as "Address ID"
                                   FROM author
                                   ORDER BY n_author_id ASC""")

    return render_template("update_author.html",
                           column_names=df_authors.columns.values, row_data=list(df_authors.values.tolist()), zip=zip)


@app.route('/execute_change_author_manually', methods=['POST', 'GET'])
def execute_change_author_manually():
    author_id = request.form['author_id']

    if author_id == "":
        return render_template("includes/fail.html", title='Author update failed',
                               text='Update failed! Reason: Missing Author identifier.')

    # Operation defined by radio button in form
    if request.form['operator'] == "delete":

        try:
            bib.exec_statement(f"""DELETE FROM author WHERE n_author_id = {author_id};""")
        except psycopg2.errors.ForeignKeyViolation:
            return render_template("includes/fail.html", title='Author deletion failed',
                                   text='Delete failed! Reason: Author still has Books associated with them.')
        except psycopg2.errors.InFailedSqlTransaction:
            return render_template("includes/fail.html", title='Author deletion failed',
                                   text='Delete failed! Reason: Author does not exist.')
        else:
            return render_template("includes/success.html", title='Author deleted',
                                   text='Author was successfully deleted.')
    else:
        param_list = [
            request.form['author_first_name'],
            request.form['author_last_name'],
            request.form['address_id']]
        # manipulating result list to include necessary nones for set_manually function
        result = list()
        for item in param_list:
            if item == "":
                result.append(None)
            else:
                result.append(item)

        if param_list[1] is None:
            old_last_name = bib.get_select(f"SELECT s_last_name FROM author WHERE n_author_id = {author_id}").iat[0, 0]
            if old_last_name != "Null":
                param_list[2] = old_last_name

        if param_list[2] is None:
            old_address_id = bib.get_select(f"SELECT n_address_id FROM author WHERE n_author_id = {author_id}").iat[
                0, 0]
            if old_address_id != "Null":
                param_list[2] = old_address_id

        prev_first_name = bib.get_select(f"SELECT s_first_name FROM AUTHOR WHERE n_author_id = {author_id}").iat[0, 0]

        result = bib.exec_statement(
            bib.Updates.update_author(author_id, new_first_name=param_list[0], prev_first_name=prev_first_name,
                                      lastname=param_list[1], address_id=param_list[2]))

        if result is True:
            return render_template("includes/success.html", title='Author updated',
                                   text='Author updated successfully')
            return render_template("includes/fail.html", title='Author update failed',
                                   text='You have not updated the author. Inputs do not comply with table restrictions')


@app.route('/update_address', methods=['POST', 'GET'])
def update_address():
    df_address = bib.get_select("""SELECT n_address_id as "Address ID",
                                          s_street as street,
                                          s_house_number as housenumber,
                                          s_city as city,
                                          n_zipcode as zipcode,
                                          s_country as country
                                   FROM addresses
                                   ORDER BY n_address_id ASC""")

    return render_template("update_address.html",
                           column_names=df_address.columns.values, row_data=list(df_address.values.tolist()), zip=zip)


@app.route('/execute_change_address_manually', methods=['POST', 'GET'])
def execute_change_address_manually():
    address_id = request.form['address_id']
    param_list = [
        request.form['street'],
        request.form['housenumber'],
        request.form['city'],
        request.form['zipcode'],
        request.form['country']]

    # Operation defined by radio button in form
    if request.form['operator'] == "delete":
        if address_id == "":
            return render_template("includes/fail.html", title='Address Deletion failed',
                                   text='Deletion failed! Reason: Missing address identifier.')

        try:
            bib.exec_statement(f'DELETE FROM ADDRESSES WHERE n_address_id = {address_id}')
        except psycopg2.errors.ForeignKeyViolation:
            return render_template("includes/fail.html", title='Address deletion failed',
                                   text='Delete failed! Reason: Address is used elsewhere.')
        except psycopg2.errors.InFailedSqlTransaction:
            return render_template("includes/fail.html", title='Address deletion failed',
                                   text='Delete failed! Reason: Address ID does not exist.')
        else:
            return render_template("includes/success.html", title='Address deleted',
                                   text='Address was successfully deleted.')

    elif request.form['operator'] == "add":
        try:
            bib.exec_statement(f"""INSERT INTO ADDRESSES 
                                        (s_street, s_house_number, 
                                        s_city, n_zipcode, 
                                        s_country)
                                   VALUES
                                        ('{param_list[0]}', {param_list[1]}, 
                                        '{param_list[2]}', {param_list[3]}, 
                                        '{param_list[4]}');""")
        except:
            return render_template("includes/fail.html", title='Address addition failed',
                                   text='Addition failed!')
        else:
            return render_template("includes/success.html", title='Address added',
                                   text='Address was successfully added.')

    elif request.form['operator'] == "update":

        result = bib.exec_statement(bib.Updates.update_address(param_list, address_id))

        if result is True:
            return render_template("includes/success.html", title='Address updated',
                                   text='Address updated successfully')
            return render_template("includes/fail.html", title='Address update failed',
                                   text='You have updated the address.')


###########################################################################


@app.route('/dev', methods=['POST', 'GET'])  # Testing
def dev():
    return render_template("_dev.html")
