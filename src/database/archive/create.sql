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
    n_address_id   SERIAL UNIQUE NOT NULL,
    s_street       VARCHAR(128)  NOT NULL,
    s_house_number VARCHAR(20)   NOT NULL,
    s_city         VARCHAR(20)   NOT NULL,
    s_country      VARCHAR(20)   NOT NULL,
    n_zipcode      INT           NOT NULL,
    PRIMARY KEY (n_address_id)
);

CREATE TABLE AUTHOR
(
    n_author_id  SERIAL UNIQUE NOT NULL,
    s_first_name VARCHAR(128),
    s_last_name  VARCHAR(128)  NOT NULL,
    n_address_id INT,
    PRIMARY KEY (n_author_id),
    FOREIGN KEY (n_address_id) REFERENCES ADDRESSES (n_address_id) ON DELETE SET NULL
);

CREATE TABLE PUBLISHER
(
    n_publisher_id SERIAL UNIQUE NOT NULL,
    s_pub_name     VARCHAR(128)  NOT NULL,
    n_address_id   INT,
    PRIMARY KEY (n_publisher_id),
    FOREIGN KEY (n_address_id) REFERENCES ADDRESSES (n_address_id) ON DELETE SET NULL
);


CREATE TABLE LIB_LOCATION
(
    n_location_id SERIAL UNIQUE NOT NULL,
    s_compartment VARCHAR(20),
    s_shelf       VARCHAR(20),
    s_room        VARCHAR(20),
    n_loc_floor   INT,
    n_address_id  INT,
    PRIMARY KEY (n_location_id),
    FOREIGN KEY (n_address_id) REFERENCES ADDRESSES (n_address_id) ON DELETE CASCADE
);



CREATE TABLE BOOKS
(
    n_book_id         SERIAL UNIQUE NOT NULL,
    s_isbn            VARCHAR(13) UNIQUE,
    s_title           VARCHAR(4096) NOT NULL,
    n_book_edition    INT           NOT NULL DEFAULT 1,
    s_genre           CHAR(20),
    n_publishing_year INT,
    s_book_language   CHAR(3),
    n_recommended_age INT,
    b_is_available    BOOL          NOT NULL,
    n_publisher_id    INT,
    n_location_id     INT,
    PRIMARY KEY (n_book_id),
    FOREIGN KEY (n_publisher_id) REFERENCES PUBLISHER (n_publisher_id) ON DELETE SET NULL,
    FOREIGN KEY (n_location_id) REFERENCES LIB_LOCATION (n_location_id) ON DELETE SET NULL
);

CREATE TABLE USERS
(
    n_user_id        SERIAL UNIQUE       NOT NULL,
    s_user_name      VARCHAR(128) UNIQUE NOT NULL,
    s_password       VARCHAR(128)        NOT NULL,
    s_first_name     VARCHAR(128),
    s_last_name      VARCHAR(128),

    dt_date_of_birth DATE,
    n_address_id     INT,
    PRIMARY KEY (n_user_id),
    FOREIGN KEY (n_address_id) REFERENCES ADDRESSES (n_address_id) ON DELETE SET NULL
);

CREATE TABLE LOAN
(
    n_loan_id SERIAL UNIQUE NOT NULL,
    ts_now    TIMESTAMP     NOT NULL DEFAULT current_timestamp,
    n_user_id INT           NOT NULL,
    PRIMARY KEY (n_loan_id),
    FOREIGN KEY (n_user_id) REFERENCES USERS (n_user_id) ON DELETE CASCADE
);


CREATE TABLE BORROW_ITEM
(
    n_borrow_item_id SERIAL UNIQUE NOT NULL,
    n_duration       INT           NOT NULL, --in days
    n_book_id        INT           NOT NULL,
    n_loan_id        INT           NOT NULL,
    b_active         BOOL          NOT NULL DEFAULT true,
    PRIMARY KEY (n_borrow_item_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id) ON DELETE CASCADE,
    FOREIGN KEY (n_loan_id) REFERENCES LOAN (n_loan_id) ON DELETE CASCADE
);


CREATE TABLE READ_BOOKS
(
    n_read_books_id SERIAL UNIQUE NOT NULL,
    n_book_id       INT           NOT NULL,
    n_user_id       INT           NOT NULL,
    PRIMARY KEY (n_read_books_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id) ON DELETE CASCADE,
    FOREIGN KEY (n_user_id) REFERENCES USERS (n_user_id) ON DELETE CASCADE
);



CREATE TABLE WROTE
(
    n_wrote_id  SERIAL UNIQUE NOT NULL,
    n_book_id   INT           NOT NULL,
    n_author_id INT           NOT NULL,
    PRIMARY KEY (n_wrote_id),
    FOREIGN KEY (n_book_id) REFERENCES BOOKS (n_book_id) ON DELETE CASCADE,
    FOREIGN KEY (n_author_id) REFERENCES AUTHOR (n_author_id) ON DELETE CASCADE
);