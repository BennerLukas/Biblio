
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

    @staticmethod
    def sql_all_bookinformation(s_book_id=None):
        if s_book_id == False:
            s_sql= """
            SELECT b.s_isbn AS ISBN, b.s_title AS Booktitle, b.n_book_edition AS Bookedition, b.s_genre AS Bookgenre,
                    b.dt_publishing_date AS Publishingdate, b.s_book_language AS Booklenguage, b.n_recommended_age AS Recommended_Age,
                    b.b_is_availalbe AS Availabilty, au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name,
                    l.s_compartment AS Location_compartment, l.s_shelf AS Location_shelf, l.s_room AS Location_room, l.n_loc_floor AS Location_floor, 
                    ad.s_street AS Location_street, ad.s_house_number AS Location_house_number, ad.s_city AS Location_city, 
                    ad.s_country AS Location_country, ad.n_zipcode AS Location_zipcode, pu.s_pub_name AS Publisher
            FROM books AS b
                LEFT JOIN wrote AS w ON b.n_book_id =  w.n_book_id
                LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
                LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
                LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id;
            """
        else:
            s_sql=f"""
            SELECT b.s_isbn AS ISBN, b.s_title AS Booktitle, b.n_book_edition AS Bookedition, b.s_genre AS Bookgenre,
                    b.dt_publishing_date AS Publishingdate, b.s_book_language AS Booklenguage, b.n_recommended_age AS Recommended_Age,
                    b.b_is_availalbe AS Availabilty, au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name,
                    l.s_compartment AS Location_compartment, l.s_shelf AS Location_shelf, l.s_room AS Location_room, l.n_loc_floor AS Location_floor, 
                    ad.s_street AS Location_street, ad.s_house_number AS Location_house_number, ad.s_city AS Location_city, 
                    ad.s_country AS Location_country, ad.n_zipcode AS Location_zipcode, pu.s_pub_name AS Publisher
            FROM books AS b
                LEFT JOIN wrote AS w ON b.n_book_id =  w.n_book_id
                LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
                LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
                LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id
            WHERE b.n_book_id = {s_book_id};
            """
        return s_sql

    @staticmethod
    def sql_user_loanhistory(s_user_id=None):
        if s_user_id == False:
            s_sql="""
            SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, l.n_loan_id AS Loan_id,
                    l.ts_now AS Loan_timestamp, bi.n_duration AS Loan_duration, bi.b_active AS Loan_active, bo.s_isbn AS Book_ISBN,
                    bo.s_title AS Book_title, bo.n_book_edition AS Book_edition
            FROM users AS u
                LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id;
            """
        else:
            s_sql=f"""
            SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, l.n_loan_id AS Loan_id,
                    l.ts_now AS Loan_timestamp, bi.n_duration AS Loan_duration, bi.b_active AS Loan_active, bo.s_isbn AS Book_ISBN,
                    bo.s_title AS Book_title, bo.n_book_edition AS Book_edition
            FROM users AS u
                LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
            WHERE u.n_user_id ={s_user_id};
            """
        return s_sql

    @staticmethod
    def sql_user_activeloans(s_user_id=None):
        if s_user_id == False:
            s_sql="""
            SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, l.n_loan_id AS Loan_id,
                    l.ts_now AS Loan_timestamp, bi.n_duration AS Loan_duration, bi.b_active AS Loan_active, bo.s_isbn AS Book_ISBN,
                    bo.s_title AS Book_title, bo.n_book_edition AS Book_edition
            FROM users AS u
                LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
            WHERE bi.b_active = 'true';
            """
        else:
            s_sql=f"""
            SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, l.n_loan_id AS Loan_id,
                    l.ts_now AS Loan_timestamp, bi.n_duration AS Loan_duration, bi.b_active AS Loan_active, bo.s_isbn AS Book_ISBN,
                    bo.s_title AS Book_title, bo.n_book_edition AS Book_edition
            FROM users AS u
                LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
            WHERE bi.b_active = 'true' and u.n_user_id = {s_user_id};
            """
        return s_sql



    @staticmethod
    def sql_books_locations(s_book_id=None):
        if s_book_id == False:
            s_sql="""
            SELECT b.s_isbn AS ISBN, b.s_title AS Booktitle, b.n_book_edition AS Bookedition, l.s_compartment AS Location_compartment, 
                    l.s_shelf AS Location_shelf, l.s_room AS Location_room, l.n_loc_floor AS Location_floor, ad.s_street AS Location_street, 
                    ad.s_house_number AS Location_house_number, ad.s_city AS Location_city, ad.s_country AS Location_country,
            ad.n_zipcode AS Location_zipcode
            FROM books AS b
                LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
                LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
            """
        else:
            s_sql=f"""
            SELECT b.s_isbn AS ISBN, b.s_title AS Booktitle, b.n_book_edition AS Bookedition, l.s_compartment AS Location_compartment, 
                    l.s_shelf AS Location_shelf, l.s_room AS Location_room, l.n_loc_floor AS Location_floor, ad.s_street AS Location_street, 
                    ad.s_house_number AS Location_house_number, ad.s_city AS Location_city, ad.s_country AS Location_country,
            ad.n_zipcode AS Location_zipcode
            FROM books AS b
                LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
                LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
            WHERE b.n_book_id = {s_book_id};
            """
        return s_sql

    @staticmethod
    def sql_books_for_certain_genre_or_language(s_genre=None, s_language=None):
        if s_genre == False and s_language == False:
            s_sql="""
            SELECT b.s_isbn AS ISBN, b.s_title AS Booktitle, b.n_book_edition AS Bookedition, 
                    b.s_genre AS Book_genre, b.s_book_language AS Book_language
            FROM books AS b;
            """
        elif s_genre == True and s_language == False:
            s_sql=f"""
            SELECT b.s_isbn AS ISBN, b.s_title AS Booktitle, b.n_book_edition AS Bookedition, 
                    b.s_genre AS Book_genre, b.s_book_language AS Book_language
            FROM books AS b
            WHERE b.s_genre = {s_genre};
            """
        elif s_genre == False and s_language == True:
            s_sql=f"""
            SELECT b.s_isbn AS ISBN, b.s_title AS Booktitle, b.n_book_edition AS Bookedition, 
                b.s_genre AS Book_genre, b.s_book_language AS Book_language
            FROM books AS b
            WHERE b.s_book_language = {s_language};
            """
        else:
            s_sql=f"""
            SELECT b.s_isbn AS ISBN, b.s_title AS Booktitle, b.n_book_edition AS Bookedition, 
                b.s_genre AS Book_genre, b.s_book_language AS Book_language
            FROM books AS b
            WHERE b.s_book_language = {s_language} and b.s_genre = {s_genre};
            """
        return s_sql
        
    @staticmethod
    def sql_count_books_per_genre_publisher_author(s_genre=False, s_publisher=False, s_author=False):
        if s_genre == False and s_publisher == False and s_author == False:
            s_sql=f"""
            SELECT  b.s_genre AS Genre, COUNT(DISTINCT(b.n_book_id)) AS Book_count
            FROM books AS b;
            """
        elif s_genre == True and s_publisher == False and s_author == False:
            s_sql=f"""
            SELECT  b.s_genre AS Genre, COUNT(DISTINCT(b.n_book_id)) AS Book_count
            FROM books AS b
            GROUP BY b.s_genre;
            """
        elif s_genre == False and s_publisher == True and s_author == False:
            s_sql=f"""
            SELECT  pu.s_pub_name AS Publisher, COUNT(DISTINCT(b.n_book_id)) AS Book_count
            FROM books AS b
                LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id
            GROUP BY pu.s_pub_name;
            """
        elif s_genre == False and s_publisher == False and s_author == True:
            s_sql=f"""
            SELECT  au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name, COUNT(DISTINCT(b.n_book_id)) AS Book_count
            FROM books AS b
                LEFT JOIN wrote AS w ON b.n_book_id =  w.n_book_id
                LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
            GROUP BY au.s_last_name, au.s_first_name;
            """
        elif s_genre == True and s_publisher == True and s_author == False:
            s_sql=f"""
            SELECT  pu.s_pub_name AS Publisher, COUNT(DISTINCT(b.n_book_id)) AS Book_count
            FROM books AS b
                LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id
            GROUP BY b.s_genre, pu.s_pub_name;
            """
        elif s_genre == False and s_publisher == True and s_author == True:
            s_sql=f"""
            SELECT  au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name, COUNT(DISTINCT(b.n_book_id)) AS Book_count
            FROM books AS b
                LEFT JOIN wrote AS w ON b.n_book_id =  w.n_book_id
                LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id
            GROUP BY pu.s_pub_name, au.s_last_name, au.s_first_name;
            """                        
        elif s_genre == True and s_publisher == False and s_author == True:
            s_sql=f"""
            SELECT  au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name, COUNT(DISTINCT(b.n_book_id)) AS Book_count
            FROM books AS b
                LEFT JOIN wrote AS w ON b.n_book_id =  w.n_book_id
                LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
            GROUP BY b.s_genre, au.s_last_name, au.s_first_name;
            """
        else:
            s_sql=f"""
            SELECT  au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name, COUNT(DISTINCT(b.n_book_id)) AS Book_count
            FROM books AS b
                LEFT JOIN wrote AS w ON b.n_book_id =  w.n_book_id
                LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id
            GROUP BY b.s_genre, pu.s_pub_name, au.s_last_name, au.s_first_name;
            """

    @staticmethod
        def sql_most_loaned_books_per_genre_publisher_author_for_user(s_genre=False, s_publisher=False, s_author=False, TOP_Count=10):
        if s_genre == False and s_publisher == False and s_author == False:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.count_borrowed_items
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre, 
                    COUNT(bi.n_borrow_item_id) AS Count_borrowed_items, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(bi.n_borrow_item_id) DESC)
                    FROM users AS u
                        LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                        LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                        LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
                    GROUP BY  u.s_first_name, u.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == True and s_publisher == False and s_author == False:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP_genre, rp.count_borrowed_items
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre, 
                    COUNT(bi.n_borrow_item_id) AS Count_borrowed_items, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(bi.n_borrow_item_id) DESC)
                    FROM users AS u
                        LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                        LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                        LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
                    GROUP BY  u.s_first_name, u.s_last_name, bo.s_genre) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == False and s_publisher == True and s_author == False:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.publisher AS TOP_publisher, rp.count_borrowed_items
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, pu.s_pub_name AS Publisher, 
                    COUNT(bi.n_borrow_item_id) AS Count_borrowed_items, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, pu.s_pub_name ORDER BY COUNT(bi.n_borrow_item_id) DESC)
                    FROM users AS u
                        LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                        LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                        LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
                        LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
                    GROUP BY  u.s_first_name, u.s_last_name, pu.s_pub_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == False and s_publisher == False and s_author == True:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.Author_first_name AS TOP_Author_first_name, rp.Author_last_name AS TOP_Author_last_name, rp.count_borrowed_items
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name,  au.s_first_name AS Author_first_name,
                au.s_last_name AS Author_last_name, COUNT(bi.n_borrow_item_id) AS Count_borrowed_items, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, au.s_first_name, au.s_last_name ORDER BY COUNT(bi.n_borrow_item_id) DESC)
                    FROM users AS u
                        LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                        LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                        LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
                        LEFT JOIN wrote AS w ON bo.n_book_id =  w.n_book_id
                        LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                    GROUP BY  u.s_first_name, u.s_last_name, au.s_first_name, au.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == True and s_publisher == True and s_author == False:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP_genre, rp.publisher AS TOP_publisher, rp.count_borrowed_items
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre, pu.s_pub_name AS Publisher, 
                    COUNT(bi.n_borrow_item_id) AS Count_borrowed_items, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(bi.n_borrow_item_id) DESC)
                    FROM users AS u
                        LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                        LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                        LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
                        LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
                    GROUP BY  u.s_first_name, u.s_last_name, bo.s_genre, pu.s_pub_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == False and s_publisher == True and s_author == True:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.publisher AS TOP_publisher,  rp.Author_first_name AS TOP_Author_first_name, rp.Author_last_name AS TOP_Author_last_name, rp.count_borrowed_items
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, pu.s_pub_name AS Publisher, 
                    u.s_last_name AS User_last_name,  au.s_first_name AS Author_first_name, COUNT(bi.n_borrow_item_id) AS Count_borrowed_items, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, pu.s_pub_name ORDER BY COUNT(bi.n_borrow_item_id) DESC)
                    FROM users AS u
                        LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                        LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                        LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
                        LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
                    GROUP BY  u.s_first_name, u.s_last_name, pu.s_pub_name) AS rp
            WHERE rank <= {TOP_Count};
            """                        
        elif s_genre == True and s_publisher == False and s_author == True:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP_genre, rp.Author_first_name AS TOP_Author_first_name, rp.Author_last_name AS TOP_Author_last_name, rp.count_borrowed_items
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre, au.s_first_name AS Author_first_name,
                au.s_last_name AS Author_last_name, COUNT(bi.n_borrow_item_id) AS Count_borrowed_items, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(bi.n_borrow_item_id) DESC)
                    FROM users AS u
                        LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                        LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                        LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
                        LEFT JOIN wrote AS w ON bo.n_book_id =  w.n_book_id
                        LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                    GROUP BY  u.s_first_name, u.s_last_name, bo.s_genre, au.s_first_name, au.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        else:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP_genre,rp.publisher AS TOP_publisher, rp.Author_first_name AS TOP_Author_first_name, rp.Author_last_name AS TOP_Author_last_name, rp.count_borrowed_items
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre,pu.s_pub_name AS Publisher, au.s_first_name AS Author_first_name,
                au.s_last_name AS Author_last_name, COUNT(bi.n_borrow_item_id) AS Count_borrowed_items, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(bi.n_borrow_item_id) DESC)
                    FROM users AS u
                        LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
                        LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
                        LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
                        LEFT JOIN wrote AS w ON bo.n_book_id =  w.n_book_id
                        LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                        LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
                    GROUP BY  u.s_first_name, u.s_last_name, bo.s_genre,pu.s_pub_name, au.s_first_name, au.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        return s_sql

    @staticmethod
    def sql_top_loans_per_book(s_genre=False, TOP_Count=None):
        if s_genre==False and TOP_Count is None:
            s_sql=f"""
            SELECT bo.s_isbn AS Book_ISBN, bo.s_title AS Book_title, COUNT(DISTINCT(bi.n_loan_id)) AS Count_loans
            FROM books AS bo
                JOIN borrow_item AS bi ON bo.n_book_id = bi.n_book_id
            GROUP BY bo.s_isbn, bo.s_title
            ORDER BY COUNT(DISTINCT(bi.n_loan_id)) DESC;
            """
        elif s_genre==True and TOP_Count is None:
            s_sql=f"""
            SELECT bo.s_genre AS Book_genre, bo.s_isbn AS Book_ISBN, bo.s_title AS Book_title, COUNT(DISTINCT(bi.n_loan_id)) AS Count_loans
            FROM books AS bo
                JOIN borrow_item AS bi ON bo.n_book_id = bi.n_book_id
            GROUP BY bo.s_genre, bo.s_isbn, bo.s_title
            ORDER BY COUNT(DISTINCT(bi.n_loan_id)) DESC;
            """
        elif s_genre==False and TOP_Count is not None:
            s_sql=f"""
            SELECT rp.Book_ISBN, rp.Book_title, rp.Count_loans
            FROM (SELECT  bo.s_isbn AS Book_ISBN, bo.s_title AS Book_title, 
                    COUNT(DISTINCT(bi.n_loan_id)) AS Count_loans,
                    rank() OVER (PARTITION BY bo.s_isbn, bo.s_title ORDER BY COUNT(DISTINCT(bi.n_loan_id)) DESC)
                    FROM books AS bo
                        JOIN borrow_item AS bi ON bo.n_book_id = bi.n_book_id
                    GROUP BY bo.s_isbn, bo.s_title) AS rp
            WHERE rank <= {TOP_Count};
            """
        else:
            s_sql=f"""
            SELECT rp.Book_genre, rp.Book_ISBN, rp.Book_title, rp.Count_loans
            FROM (SELECT bo.s_genre AS Book_genre, bo.s_isbn AS Book_ISBN, bo.s_title AS Book_title, 
                    COUNT(DISTINCT(bi.n_loan_id)) AS Count_loans,
                    rank() OVER (PARTITION BY bo.s_genre, bo.s_isbn, bo.s_title ORDER BY COUNT(DISTINCT(bi.n_loan_id)) DESC)
                    FROM books AS bo
                        JOIN borrow_item AS bi ON bo.n_book_id = bi.n_book_id
                    GROUP BY bo.s_genre, bo.s_isbn, bo.s_title) AS rp
            WHERE rank <= {TOP_Count};
            """
        return s_sql


    @staticmethod
    def sql_total_loans_per_user():
        s_sql="""
        SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, COUNT(DISTINCT(l.n_loan_id)) AS COUNT_Loans
        FROM users AS u
            LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
            LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
            LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
        GROUP BY  u.s_first_name, u.s_last_name;
        """
        return s_sql


    @staticmethod
        def sql_most_read_books_per_genre_publisher_author(s_genre=False, s_publisher=False, s_author=False, TOP_Count=10):
        if s_genre == False and s_publisher == False and s_author == False:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.count_read_books
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name,  
                    COUNT(r.n_read_books_id) AS Count_read_books, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(r.n_read_books_id) DESC)
                    FROM users AS u
                        LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
                        LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
                    GROUP BY  u.s_first_name, u.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == True and s_publisher == False and s_author == False:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP_genre, rp.count_read_books
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre, 
                    COUNT(r.n_read_books_id) AS Count_read_books, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(r.n_read_books_id) DESC)
                    FROM users AS u
                        LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
                        LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
                    GROUP BY  u.s_first_name, u.s_last_name, bo.s_genre) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == False and s_publisher == False and s_author == True:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name,  rp.Author_first_name AS TOP_Author_first_name,
            rp.Author_last_name AS TOP_Author_last_name, rp.count_read_books
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name,
                au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name,
                    COUNT(r.n_read_books_id) AS Count_read_books, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, au.s_first_name, au.s_last_name ORDER BY COUNT(r.n_read_books_id) DESC)
                    FROM users AS u
                        LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
                        LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
                        LEFT JOIN wrote AS w ON bo.n_book_id =  w.n_book_id
                        LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                    GROUP BY  u.s_first_name, u.s_last_name, au.s_first_name, au.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == False and s_publisher == True and s_author == False:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.publisher AS TOP_publisher, rp.count_read_books
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name,
                pu.s_pub_name AS Publisher,COUNT(r.n_read_books_id) AS Count_read_books, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, pu.s_pub_name ORDER BY COUNT(r.n_read_books_id) DESC)
                    FROM users AS u
                        LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
                        LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
                        LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
                    GROUP BY  u.s_first_name, u.s_last_name, pu.s_pub_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == True and s_publisher == True and s_author == False:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP_genre, rp.publisher AS TOP_publisher, rp.count_read_books
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre, 
                    pu.s_pub_name AS Publisher,COUNT(r.n_read_books_id) AS Count_read_books, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(r.n_read_books_id) DESC)
                    FROM users AS u
                        LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
                        LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
                        LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
                    GROUP BY  u.s_first_name, u.s_last_name, bo.s_genre, pu.s_pub_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        elif s_genre == False and s_publisher == True and s_author == True:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.publisher AS TOP_publisher,  rp.Author_first_name AS TOP_Author_first_name, rp.Author_last_name AS TOP_Author_last_name,rp.count_read_books
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name,
                pu.s_pub_name AS Publisher, au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name, COUNT(r.n_read_books_id) AS Count_read_books, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, pu.s_pub_name ORDER BY COUNT(r.n_read_books_id) DESC)
                    FROM users AS u
                        LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
                        LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
                        LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
                        LEFT JOIN wrote AS w ON bo.n_book_id =  w.n_book_id
                        LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                    GROUP BY  u.s_first_name, u.s_last_name, pu.s_pub_name,au.s_first_name, au.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """                        
        elif s_genre == True and s_publisher == False and s_author == True:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP_genre, rp.Author_first_name AS TOP_Author_first_name, rp.Author_last_name AS TOP_Author_last_name, rp.count_read_books
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre, 
                    au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name, COUNT(r.n_read_books_id) AS Count_read_books, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(r.n_read_books_id) DESC)
                    FROM users AS u
                        LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
                        LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
                        LEFT JOIN wrote AS w ON bo.n_book_id =  w.n_book_id
                        LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                    GROUP BY  u.s_first_name, u.s_last_name, bo.s_genre, au.s_first_name, au.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """
        else:
            s_sql=f"""
            SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP_genre, rp.publisher AS TOP_publisher,  rp.Author_first_name AS TOP_Author_first_name, rp.Author_last_name AS TOP_Author_last_name,rp.count_read_books
            FROM (SELECT u.s_first_name AS User_first_name, u.s_last_name AS User_last_name, bo.s_genre AS Genre,
                pu.s_pub_name AS Publisher, au.s_first_name AS Author_first_name, au.s_last_name AS Author_last_name, COUNT(r.n_read_books_id) AS Count_read_books, 
                    rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, pu.s_pub_name ORDER BY COUNT(r.n_read_books_id) DESC)
                    FROM users AS u
                        LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
                        LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
                        LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
                        LEFT JOIN wrote AS w ON bo.n_book_id =  w.n_book_id
                        LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
                    GROUP BY  u.s_first_name, u.s_last_name, bo.s_genre, pu.s_pub_name,au.s_first_name, au.s_last_name) AS rp
            WHERE rank <= {TOP_Count};
            """