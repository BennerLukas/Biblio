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



CREATE TABLE ADDRESSES
(
address_id	 	SERIAL UNIQUE		NOT NULL,
street 			VARCHAR(20) 		NOT NULL,
house_number	VARCHAR(20) 		NOT NULL,
city			VARCHAR(20) 	    NOT NULL,
country			VARCHAR(20) 		NOT NULL,
zipcode			INT					NOT NULL,
PRIMARY KEY (address_id) 
);

CREATE TABLE AUTHOR
(
author_id 	SERIAL UNIQUE		NOT NULL,
first_name 	VARCHAR(20) 		NOT NULL,
last_name 	VARCHAR(20)			NOT NULL,
address_id	INT,
PRIMARY KEY (author_id),
FOREIGN KEY (address_id) REFERENCES ADDRESSES(address_id) 
);

CREATE TABLE PUBLISHER
(
publisher_id 	SERIAL UNIQUE		NOT NULL,
pub_name 		VARCHAR(20) 	NOT NULL,
address_id		INT,
PRIMARY KEY (publisher_id),
FOREIGN KEY (address_id) REFERENCES ADDRESSES(address_id) 
);


CREATE TABLE LIB_LOCATION
(
location_id 	SERIAL UNIQUE		NOT NULL,
compartment 	VARCHAR(20),
shelf			VARCHAR(20),
room			VARCHAR(20),
loc_floor		VARCHAR(20),
address_id		INT,
PRIMARY KEY (location_id),
FOREIGN KEY (address_id) REFERENCES ADDRESSES(address_id) 
);



CREATE TABLE BOOKS
( 
book_id           SERIAL UNIQUE		NOT NULL,
isbn              VARCHAR(13),
title             VARCHAR(4096)    NOT NULL,
book_edition      INT,
genre             CHAR(20),
publishing_date   DATE,
book_language     CHAR(3),
recommended_age   INT,
is_availalbe      BOOL             NOT NULL,
publisher_id      INT,
location_id       INT,
PRIMARY KEY (book_id),
FOREIGN KEY (publisher_id) REFERENCES PUBLISHER(publisher_id),
FOREIGN KEY (location_id) REFERENCES LIB_LOCATION(location_id)
);

CREATE TABLE USERS
(
user_id         SERIAL UNIQUE		NOT NULL,
first_name      VARCHAR(20)         NOT NULL,
last_name       VARCHAR(20)         NOT NULL,
date_of_birth   DATE,
address_id      INT,
PRIMARY KEY (user_id),
FOREIGN KEY (address_id) REFERENCES ADDRESSES(address_id)
);

CREATE TABLE LOAN
( 
loan_id           SERIAL UNIQUE		NOT NULL,
timestamp         TIMESTAMP        NOT NULL DEFAULT current_timestamp,
user_id           INT              NOT NULL,
PRIMARY KEY   (loan_id),
FOREIGN KEY (user_id) REFERENCES USERS(user_id) 
);


CREATE TABLE BORROW_ITEM
(
borrow_item_id    SERIAL UNIQUE		NOT NULL,
duration          INT              NOT NULL,
book_id           INT              NOT NULL,
loan_id           INT              NOT NULL,
PRIMARY KEY (borrow_item_id),
FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
FOREIGN KEY (loan_id) REFERENCES LOAN(loan_id)
);


CREATE TABLE READ_BOOKS
(
read_books_id   SERIAL UNIQUE		NOT NULL,
book_id         INT                 NOT NULL,
user_id         INT                 NOT NULL,
PRIMARY KEY (read_books_id),
FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
FOREIGN KEY (user_id) REFERENCES USERS(user_id)
);



CREATE TABLE WROTE
(
wrote_id        SERIAL UNIQUE		NOT NULL,
book_id         INT                 NOT NULL,
author_id       INT                 NOT NULL,
PRIMARY KEY (wrote_id),
FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
FOREIGN KEY (author_id) REFERENCES AUTHOR(author_id)
);
