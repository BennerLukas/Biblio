DROP VIEW IF EXISTS overview;
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



DROP VIEW IF EXISTS book_extended;
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