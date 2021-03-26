import sqlalchemy
import psycopg2
import psycopg2.extras
import pandas as pd
import logging
import re

from api.selections import Selections
from api.updates import Updates


class Biblio:

    def __init__(self):
        self.s_user = None
        self.s_user = 1

        self.alchemy_engine = None
        self.alchemy_connection = None
        self.psycopg2_connection = None

        self.b_connected = False
        self.b_initialised = False

        self.Selections = Selections()
        self.Updates = Updates()

        self.connect()

    # ###########################################################################################################
    # INIT FUNCTIONS

    def connect(self):
        """
        makes a sqlalchemy and psycopg2 connection to the db.

        :return:
        """
        try:
            self.alchemy_engine = sqlalchemy.create_engine('postgres+psycopg2://postgres:1234@localhost:5433/postgres')
            self.alchemy_connection = self.alchemy_engine.connect()
            self.psycopg2_connection = psycopg2.connect(database="postgres", user="postgres", port=5433,
                                                        password="1234",
                                                        host="localhost")
            self.b_connected = True
            print("Database Connected")
            logging.info("Connected to DB")
        except Exception as an_exception:
            logging.error(an_exception)
            logging.error("Not connected to DB")
        return True

    def test(self, b_verbose=True):
        """
        tests the connection to the db.

        :param b_verbose:
        :return:
        """
        # needs data to query; use init_db() beforehand.
        if self.b_connected:
            df = pd.read_sql_query('SELECT * FROM books LIMIT 1', self.alchemy_connection)
            if b_verbose:
                print(df)
            return df
        return False

    def init_db(self):
        """
        --CAUTION--

        DELETES ALL EXISTING DATA

        Initializes the db with from the ground up and adds some default data.

        :return:
        """
        if self.b_connected:
            s_sql_statement = open("../../database/init.sql", "r").read()
            s_sql_statement = re.sub(r"--.*|\n|\t", " ",
                                     s_sql_statement)  # cleaning file from comments and escape functions

            self.alchemy_connection.execute(s_sql_statement)

            logging.info("Database initialised")
            print("Database initialised")
            self.b_initialised = True
            return True

    # ###########################################################################################################
    # USING FUNCTIONS

    def get_select(self, s_sql_statement: str) -> object:
        """
        This Function needs a Select-Statements and returns the result in a df.

        :param s_sql_statement:
        :return df:
        """
        try:
            df = pd.read_sql_query(s_sql_statement, self.alchemy_connection)
        except Exception as an_exception:
            logging.error(an_exception)
            logging.error("Query couldn't be executed.")
            return False
        return df

    def exec_statement(self, sql: str):
        """
        can execute every kind of Sql-statement but does NOT return a response.

        Use for:
            - CALL Procedure
            - UPDATE Statement
        :param sql:
        :return:
        """
        db_cursor = self.psycopg2_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        db_cursor.execute(sql)
        self.psycopg2_connection.commit()
        db_cursor.close()
        return True

    # ###########################################################################################################
    # EXECUTING FUNCTIONS

    def set_user(self, s_username, s_pwd):
        s_sql = f"SELECT n_user_id FROM users WHERE s_user_name = '{s_username}' AND s_password = '{s_pwd}'"
        df = self.get_select(s_sql)
        n_id = int(df['n_user_id'])
        self.s_user = n_id
        return self.s_user

    def get_book_id_by_isbn(self, isbn):
        s_sql = f"SELECT n_book_id FROM books WHERE s_isbn = '{isbn}'"
        df = self.get_select(s_sql)
        if df.shape == (1, 1):
            n_id = int(df['n_book_id'])
            return n_id
        return False

    def get_book_id_by_title_edition(self, title, edition=1):
        s_sql = f"SELECT n_book_id FROM books WHERE s_title = '{title}' AND n_book_edition = {edition}"
        df = self.get_select(s_sql)
        if df.shape == (1, 1):
            n_id = int(df['n_book_id'])
            return n_id
        return False

    def mark_book_as_read(self, book_id):
        s_insert = f"INSERT INTO READ_BOOKS(n_book_id, n_user_id) VALUES ({book_id}, {self.s_user});"
        self.exec_statement(s_insert)
        return True

    def return_book(self, book_id):
        try:
            s_update = f"UPDATE borrow_item SET b_active = false WHERE n_book_id = {book_id};"
            self.exec_statement(s_update)
            logging.info(f"Book {book_id} returned")
        except Exception as an_exception:
            logging.error(an_exception)
            logging.error("Book couldn't be returned.")
            return False
        return True

    def make_loan(self, book_ids, duration=14):
        try:
            if isinstance(book_ids, int):
                book_ids = [book_ids]
            idx = -1
            for book_id in book_ids:
                idx += 1
                s_sql = f"SELECT b_is_available FROM BOOKS WHERE n_book_id = {book_id}"
                df = self.get_select(s_sql)
                if df.shape == (1, 1):
                    b_is_available = df['b_is_available'].values[0]
                else:
                    continue
                if bool(b_is_available) is False:
                    # return book
                    result = self.return_book(book_id)
                    if result is True:
                        book_ids.pop(idx)
                    continue
            if len(book_ids) == 0:
                return True
            call = f"CALL new_loan({self.s_user}, ARRAY{book_ids}, {duration});"
            self.exec_statement(call)
        except Exception as an_exception:
            logging.error(an_exception)
            logging.error("Book couldn't be loaned.")
            return False
        return True

    def add_new_book(self, obj_book):
        try:
            call = obj_book.get_s_sql_call()
            self.exec_statement(call)
        except Exception as an_exception:
            logging.error(an_exception)
            logging.error("Book couldn't be loaned.")
            return False
        return True

    # ############################################################################################################


if __name__ == "__main__":
    my_class = Biblio()
    my_class.init_db()
    # my_class.get_book_id_by_isbn(9780575097568)
    # my_class.test(True)
    # my_class.list_read_books()
    # my_class.make_loan([1, 2], 14)
    # my_class.return_book(1)
