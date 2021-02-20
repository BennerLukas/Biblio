
class Selections:

    def __init__(self):
        pass

    @staticmethod
    def sql_exceeded_loans():
        s_sql = """
        SELECT bi.n_borrow_item_id AS Borrowed_item, bi.n_loan_id AS Loan_id, bi.n_duration + DATE(l.ts_now) AS Due_Date
        FROM borrow_item AS bi
        LEFT JOIN loan AS l ON bi.n_loan_id = l.n_loan_id
        WHERE CURRENT_DATE > bi.n_duration + DATE(l.ts_now) AND bi.b_active = 'TRUE';
        """
        return s_sql
    
    @staticmethod
    def sql_read_books(s_user):
        s_book_ids = f'SELECT n_book_id FROM read_books WHERE n_user_id = {s_user}'
        s_sql = f'SELECT title, author, publisher, isbn FROM overview WHERE bookid IN ({s_book_ids});' 
        return s_sql
