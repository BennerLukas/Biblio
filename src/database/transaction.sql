DECLARE 
        author_first_name   VARCHAR(128)    := 'Klaus'
        author_last_name    VARCHAR(128)    := 'Kleber';
        author_address      INT             :=  NULL;       
        publisher_name      VARCHAR(128)    := 'K-Verlag';
        publisher_address   INT             :=  NULL;       
        book_title          VARCHAR(4096)   := 'Die Suche';
        book_edition        INT             :=  1;
        book_language       CHAR(3)         := 'DE';
        book_genre          CHAR(20)        := 'Fantasy';
        book_isbn           VARCHAR(13)     := '1234567891234';

-- without addresses

BEGIN
    IF NOT EXISTS   (   SELECT n_author_id
                    FROM author
                    WHERE   author_last_name = s_last_name
                    AND     author_first_name = s_first_name)
                )
    BEGIN
        INSERT INTO AUTHOR(s_first_name, s_last_name, n_address_id)
        VALUES (author_first_name, author_last_name, author_address)
    END

    IF NOT EXITS    (   SELECT n_publisher_id
                        FROM PUBLISHER
                        WHERE publisher_name = s_pub_name)
    BEGIN
        INSERT INTO PUBLISHER(s_pub_name, n_address_id)
        VALUES (publisher_name, publisher_address)
    END

    IF NOT EXISTS   (   SELECT n_book_id
                        FROM books
                        WHERE   book_isbn = s_isbn
                        OR      (book_title = s_title AND book_edition = n_book_edition AND book_language = s_book_language)
                        )
    BEGIN
        INSERT INTO BOOKS(s_isbn, s_title, n_book_edition, s_genre, dt_publishing_date, s_book_language, n_recommended_age, b_is_availalbe, n_publisher_id, n_location_id)
        VALUES  (   book_isbn, 
                    book_title,  
                    book_edition, 
                    book_genre, 
                    NULL, 
                    book_language, 
                    NULL, 
                    true, 
                    (SELECT n_author_id FROM author WHERE   author_last_name = s_last_name AND author_first_name = s_first_name),
                    (SELECT n_publisher_id FROM PUBLISHER WHERE publisher_name = s_pub_name)
                    )
    END

END;