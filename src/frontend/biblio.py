import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import logging

class Biblio:

    def __init__(self):
        self.s_user = None

        self.engine = None
        self.connection = None
        self.cursor = None
        self.b_connected = False

        self.connect()

    def connect(self):
        try:
            self.engine = create_engine('postgres+psycopg2://postgres:1234@localhost:5433/postgres')
            self.connection = self.engine.raw_connection()
            self.cursor = self.connection.cursor()
            self.b_connected = True
            logging.info("Connected to DB")
        except:
            logging.error("Not connected to DB")
            return False
        return True

    def init_db(self):
        pass

    def list_read_books(self):
        
        books = []
        return books
    
    def make_loan(self, book_ids, duration):
        
        return True

    def return_book(self, book_id):
        
        return True

if __name__ == "__main__":
    my_class = Biblio()