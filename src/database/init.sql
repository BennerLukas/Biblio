-- CREATE; PROCEDURE; TRIGGER; TRANSACTION; VIEW; 
-- Missing: SELECT; INSERT; 

-- Drop all old
DROP VIEW IF EXISTS overview;
DROP VIEW IF EXISTS book_extended;
DROP TRIGGER IF EXISTS book_returned ON BORROW_ITEM;
DROP TABLE IF EXISTS WROTE;
DROP TABLE IF EXISTS READ_BOOKS;
DROP TABLE IF EXISTS BORROW_ITEM;
DROP TABLE IF EXISTS LOAN;
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS BOOKS;
DROP TABLE IF EXISTS LIB_LOCATION;
DROP TABLE IF EXISTS PUBLISHER;
DROP TABLE IF EXISTS AUTHOR;
DROP TABLE IF EXISTS ADDRESSES;


-- Create tables
CREATE TABLE ADDRESSES
(
n_address_id	 	SERIAL UNIQUE		NOT NULL,
s_street 			VARCHAR(128) 		NOT NULL,
s_house_number	VARCHAR(20) 		    NOT NULL,
s_city			VARCHAR(20) 	        NOT NULL,
s_country			VARCHAR(20) 		NOT NULL,
n_zipcode			INT					NOT NULL,
PRIMARY KEY (n_address_id) 
);

CREATE TABLE AUTHOR
(
n_author_id 	SERIAL UNIQUE		NOT NULL,
s_first_name 	VARCHAR(128) 		NOT NULL,
s_last_name   VARCHAR(128)			NOT NULL,
n_address_id	INT,
PRIMARY KEY (n_author_id),
FOREIGN KEY (n_address_id) REFERENCES ADDRESSES(n_address_id) 
);

CREATE TABLE PUBLISHER
(
n_publisher_id 	SERIAL UNIQUE		NOT NULL,
s_pub_name 		VARCHAR(128) 	NOT NULL,
n_address_id		INT,
PRIMARY KEY (n_publisher_id),
FOREIGN KEY (n_address_id) REFERENCES ADDRESSES(n_address_id) 
);


CREATE TABLE LIB_LOCATION
(
n_location_id 	SERIAL UNIQUE		NOT NULL,
s_compartment 	VARCHAR(20),
s_shelf			VARCHAR(20),
s_room			VARCHAR(20),
n_loc_floor		INT,
n_address_id		INT,
PRIMARY KEY (n_location_id),
FOREIGN KEY (n_address_id) REFERENCES ADDRESSES(n_address_id) 
);



CREATE TABLE BOOKS
( 
n_book_id           SERIAL UNIQUE		NOT NULL,
s_isbn              VARCHAR(13),
s_title             VARCHAR(4096)    NOT NULL,
n_book_edition      INT,
s_genre             CHAR(20),
dt_publishing_date   DATE,
s_book_language     CHAR(3),
n_recommended_age   INT,
b_is_availalbe      BOOL             NOT NULL,
n_publisher_id      INT,
n_location_id       INT,
PRIMARY KEY (n_book_id),
FOREIGN KEY (n_publisher_id) REFERENCES PUBLISHER(n_publisher_id),
FOREIGN KEY (n_location_id) REFERENCES LIB_LOCATION(n_location_id)
);

CREATE TABLE USERS
(
n_user_id         SERIAL UNIQUE		NOT NULL,
s_first_name      VARCHAR(128)         NOT NULL,
s_last_name       VARCHAR(128)         NOT NULL,
dt_date_of_birth   DATE,
n_address_id      INT,
PRIMARY KEY (n_user_id),
FOREIGN KEY (n_address_id) REFERENCES ADDRESSES(n_address_id)
);

CREATE TABLE LOAN
( 
n_loan_id           SERIAL UNIQUE	 NOT NULL,
ts_now         TIMESTAMP             NOT NULL DEFAULT current_timestamp,
n_user_id           INT              NOT NULL,
PRIMARY KEY   (n_loan_id),
FOREIGN KEY (n_user_id) REFERENCES USERS(n_user_id) 
);


CREATE TABLE BORROW_ITEM
(
n_borrow_item_id    SERIAL UNIQUE	 NOT NULL,
n_duration          INT              NOT NULL,  --in days
n_book_id           INT              NOT NULL,
n_loan_id           INT              NOT NULL,
b_active            BOOL           NOT NULL DEFAULT true,
PRIMARY KEY (n_borrow_item_id),
FOREIGN KEY (n_book_id) REFERENCES BOOKS(n_book_id),
FOREIGN KEY (n_loan_id) REFERENCES LOAN(n_loan_id)
);


CREATE TABLE READ_BOOKS
(
n_read_books_id   SERIAL UNIQUE		NOT NULL,
n_book_id         INT               NOT NULL,
n_user_id         INT               NOT NULL,
PRIMARY KEY (n_read_books_id),
FOREIGN KEY (n_book_id) REFERENCES BOOKS(n_book_id),
FOREIGN KEY (n_user_id) REFERENCES USERS(n_user_id)
);



CREATE TABLE WROTE
(
n_wrote_id        SERIAL UNIQUE		NOT NULL,
n_book_id         INT                 NOT NULL,
n_author_id       INT                 NOT NULL,
PRIMARY KEY (n_wrote_id),
FOREIGN KEY (n_book_id) REFERENCES BOOKS(n_book_id),
FOREIGN KEY (n_author_id) REFERENCES AUTHOR(n_author_id)
);




-- Create views
CREATE VIEW overview AS
SELECT  books.s_title Title, 
        books.s_genre Genre,
        books.s_isbn Isbn, 
        STRING_AGG (s_last_name, ', ') Author, 
        s_pub_name Publisher
FROM books
LEFT JOIN wrote ON (books.n_book_id = wrote.n_book_id)
LEFT JOIN author ON (wrote.n_author_id = author.n_author_id)
LEFT JOIN publisher ON (books.n_publisher_id = publisher.n_publisher_id)
GROUP BY books.n_book_id, s_pub_name;

CREATE VIEW book_extended AS
SELECT      books.n_book_id, 
            books.s_isbn, 
            books.s_title , 
            books.n_book_edition, 
            books.s_genre, 
            books.dt_publishing_date, 
            books.s_book_language, 
            books.n_recommended_age, 
            books.b_is_availalbe, 
            author.s_first_name, 
            author.s_last_name, 
            publisher.s_pub_name
FROM books
LEFT JOIN wrote ON (books.n_book_id = wrote.n_book_id)
LEFT JOIN author ON (wrote.n_author_id = author.n_author_id)
LEFT JOIN publisher ON (books.n_publisher_id = publisher.n_publisher_id)
GROUP BY books.n_book_id, wrote.n_wrote_id, author.n_author_id, publisher.n_publisher_id;



-- Create procedures
create or replace procedure add_book( 
    author_first_name   VARCHAR(128),
    author_last_name    VARCHAR(128),
    author_address      INT,
    publisher_name      VARCHAR(128),
    publisher_address   INT,
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
                    AND     author_first_name = s_first_name
                )
    THEN
        INSERT INTO AUTHOR(s_first_name, s_last_name, n_address_id)
        VALUES (author_first_name, author_last_name, author_address);
    END IF;

    IF NOT EXISTS    (   SELECT n_publisher_id
                        FROM PUBLISHER
                        WHERE publisher_name = s_pub_name)
    THEN
        INSERT INTO PUBLISHER(s_pub_name, n_address_id)
        VALUES (publisher_name, publisher_address);
    END IF;

    IF NOT EXISTS   (   SELECT n_book_id
                        FROM books
                        WHERE   book_isbn = s_isbn
                        OR      (book_title = s_title AND book_edition = n_book_edition AND book_language = s_book_language)
                        )
    THEN
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
                    );
    END IF;

END;'
;

CREATE OR REPLACE FUNCTION book_returned_triggered()
	RETURNS TRIGGER
	LANGUAGE PLPGSQL
	AS '
		BEGIN			
			IF new.b_active <> old.b_active then
				UPDATE books
			   SET b_is_availalbe = true
		   	WHERE books.n_book_id = new.n_book_id;
	   	END if;
	   	
	   	RETURN NEW;
		END;
		';


-- Create trigger
CREATE TRIGGER book_returned 
AFTER UPDATE
ON borrow_item
FOR EACH ROW
EXECUTE PROCEDURE book_returned_triggered();

