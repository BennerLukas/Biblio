
create or replace procedure add_book( 
    author_first_name   VARCHAR(128),
    author_last_name    VARCHAR(128),
    author_address      INT;      ,
    publisher_name      VARCHAR(128),
    publisher_address   INT;      ,
    book_title          VARCHAR(4096),
    book_edition        INT,
    book_language       CHAR(3),
    book_genre          CHAR(20),
    book_isbn           VARCHAR(13)
)
-- without addresses
language plpgsql
AS '
BEGIN
    IF NOT EXISTS   (   SELECT n_author_id
                    FROM author
                    WHERE   author_last_name = s_last_name
                    AND     author_first_name = s_first_name)
                )
    THEN
        INSERT INTO AUTHOR(s_first_name, s_last_name, n_address_id)
        VALUES (author_first_name, author_last_name, author_address)
    END IF;

    IF publisher_name IS NOT NULL THEN
        IF NOT EXITS    (   SELECT n_publisher_id
                            FROM PUBLISHER
                            WHERE publisher_name = s_pub_name)
        THEN
            INSERT INTO PUBLISHER(s_pub_name, n_address_id)
            VALUES (publisher_name, publisher_address)
        END IF;
    END IF;

    IF NOT EXISTS   (   SELECT n_book_id
                        FROM books
                        WHERE   book_isbn = s_isbn
                        OR      (book_title = s_title AND book_edition = n_book_edition AND book_language = s_book_language)
                        )
    THEN
        INSERT INTO BOOKS(s_isbn, s_title, n_book_edition, s_genre, n_publishing_date, s_book_language, n_recommended_age, b_is_availalbe, n_publisher_id, n_location_id)
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
    END IF

COMMIT;'
;