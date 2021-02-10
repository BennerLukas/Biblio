import sqlalchemy


class Biblio:

    def __init__(self):
        self.s_user = None
        self.b_is_connected = False

    def connect(self):
        pass

    def list_read_books(self):
        
        books = []
        return books
    
    def make_loan(self, book_ids, duration):
        
        return True

    def return_book(self, book_id):
        
        return True