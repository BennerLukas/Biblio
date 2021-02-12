import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import logging
import re

class Biblio:

    def __init__(self):
        self.s_user = None

        self.engine = None
        self.connection = None
        self.cursor = None

        self.b_connected = False
        self.b_initialised = False

        self.connect()

    def connect(self):
        try:
            self.engine = create_engine('postgres+psycopg2://postgres:1234@localhost:5433/postgres')
            self.connection = self.engine.connect()
            # self.cursor = self.connection.cursor()
            self.b_connected = True
            print("Done")
            logging.info("Connected to DB")
        except:
            logging.error("Not connected to DB")
        return True

    def test(self, b_verbose=True):
        
        if self.b_connected and self.b_initialised:
            df = pd.read_sql_query('SELECT * FROM books LIMIT 1', self.connection)
            if b_verbose:
                print(df)
            return df

        return False

    def init_db(self):
        if self.b_connected:
            s_sql_statement = open(r"src\database\init.sql", "r").read()
            s_sql_statement = re.sub(r"--.*|\n|\t", " ", s_sql_statement)

            self.connection.execute(str(s_sql_statement))

            logging.info("Database initialised")
            self.b_initialised = True
            return True

    def list_read_books(self):
        
        books = []
        return books
    
    def make_loan(self, book_ids, duration):
        
        return True

    def return_book(self, book_id):
        
        return True



if __name__ == "__main__":
    my_class = Biblio()
    # my_class.test()
    my_class.init_db()