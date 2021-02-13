import sqlalchemy
import pandas as pd
import logging
import re

from selections import Selections

class Biblio:

    def __init__(self):
        self.s_user = None
        self.s_user = 1

        self.engine = None
        self.connection = None
        self.cursor = None

        self.b_connected = False
        self.b_initialised = False

        self.Selections = Selections()

        self.connect()

    def connect(self):
        try:
            self.engine = sqlalchemy.create_engine('postgres+psycopg2://postgres:1234@localhost:5433/postgres')
            self.connection = self.engine.connect()
            # self.cursor = self.connection.cursor()
            self.b_connected = True
            print("Done")
            logging.info("Connected to DB")
        except:
            logging.error("Not connected to DB")
        return True

    def test(self, b_verbose=True):
        # needs data to query; use init_db() beforehand.
        if self.b_connected:
            df = pd.read_sql_query('SELECT * FROM books LIMIT 1', self.connection)
            if b_verbose:
                print(df)
            return df
        return False

    def init_db(self):
        if self.b_connected:
            s_sql_statement = open(r"src\database\init.sql", "r").read()
            s_sql_statement = re.sub(r"--.*|\n|\t", " ", s_sql_statement)   # cleaning file from comments and escape functions

            self.connection.execute(s_sql_statement)

            logging.info("Database initialised")
            self.b_initialised = True
            return True

    def get_select(self, s_sql_statement):
        try:
            df = pd.read_sql_query(s_sql_statement, self.connection)
        except:
            logging.error("Query couldn't be executed.")
            return False
        return df

    def list_read_books(self):
        df = self.get_select(self.Selections.sql_read_books(self.s_user))
        print(df)
        return

    def return_book(self, book_id):
        try:
            s_update = f'UPDATE borrow_item SET b_active = false WHERE n_book_id = {book_id};'
            self.connection.execute(s_update)
            logging.info(f"Book {book_id} returned")
        except:
            logging.error("Book couldn't be returned. Try again.")
            return False
        return True

    def get_select(self, s_sql_statement):
        try:
           df = pd.read_sql_query(s_sql_statement, self.connection)
        except:
            logging.error("Query couldn't be executed.")
            return False
        return df


    def make_loan(self, book_ids, duration):
        
        call = f"CALL new_loan({self.s_user}, ARRAY{book_ids}, {duration});"

        # results = self.cursor.callproc('new_loan', [self.s_user, book_ids, duration])

        # results = self.connection.execute(f'CALL new_loan({self.s_user}, ARRAY{book_ids}, {duration});')
        # results = self.connection.execute(f'SELECT {"b_active"} from {"borrow_items"};')
        self.engine

        # print(results)
        return True



    def add_new_book(self, obj_book):
        pass


if __name__ == "__main__":
    my_class = Biblio()
    my_class.init_db()
    my_class.list_read_books()
    # my_class.return_book(2)
    # my_class.make_loan([4], 22)
    # my_class.test()
