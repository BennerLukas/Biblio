class Updates:

    def __init__(self):
        pass

    @staticmethod
    def format_sql_string(sql_str) -> str:
        sql_str = sql_str.replace("'None'", "NULL").replace("None", "NULL")
        return sql_str

    @staticmethod
    def update_book(self, book_obj, book_id=None) -> str:
        s_update = f''' UPDATE books
                        SET (n_book_edition, s_genre, n_publishing_year,
                            s_book_language, n_recommended_age, n_location_id) =
                            ({book_obj.book_edition}, {book_obj.book_genre}, {book_obj.publishing_year},
                             {book_obj.book_language}, {book_obj.reco_age}, {book_obj.location_id})
                        WHERE n_book_id = (
                            SELECT n_book_id
                            FROM books
                            WHERE s_title = {book_obj.book_title} AND n_book_edition = {book_obj.book_edition})
                                OR n_book_id = {book_id};'''

        s_update = self.format_sql_string(s_update)
        return s_update

    @staticmethod
    def delete_book(self, book_id):
        s_delete = f"""
                        DELETE FROM wrote WHERE n_book_id = {book_id};
                        DELETE FROM books WHERE n_book_id = {book_id};
        """
        return s_delete

    @staticmethod
    def update_author(self, author_id=None, new_first_name=None, prev_first_name=None, lastname=None,
                      address_id=None) -> str:

        if author_id is None:
            s_update = f''' UPDATE author
                            SET (s_first_name, n_address_id) = ( '{new_first_name}', {address_id})
                            WHERE n_author_id = ( 
                                SELECT n_author_id 
                                FROM author 
                                WHERE s_last_name = '{lastname}' AND s_first_name = '{prev_first_name})';'''
        else:
            s_update = f"""UPDATE author
                           SET (s_first_name, s_last_name, n_address_id) = ( '{new_first_name}', '{lastname}', {address_id} ) 
                           WHERE n_author_id = {author_id}"""
        s_update = self.format_sql_string(s_update)
        return s_update

    @staticmethod
    def update_publisher(self, publisher_name=None, address_id=None) -> str:
        s_update = f''' UPDATE publisher
                        SET (n_address_id) = ({address_id})
                        WHERE n_publisher_id = ( 
                            SELECT n_publisher_id 
                            FROM publisher 
                            WHERE s_pub_name = {publisher_name});'''
        s_update = self.format_sql_string(s_update)
        return s_update

    @staticmethod
    def update_address(self, parameters, address_id):
        s_update = f"""UPDATE address
                       SET (s_street, s_house_number, s_city, n_zipcode, s_country) =
                       ('{parameters[0]}', '{parameters[1]}', '{parameters[2]}', '{parameters[3]}', '{parameters[4]}'
                       WHERE n_address_id = {address_id}"""
        s_update = self.format_sql_string(s_update)
        return s_update
