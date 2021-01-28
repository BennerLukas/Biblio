DROP VIEW IF EXISTS overview;
CREATE VIEW overview AS
SELECT s_title 'Title', s_genre, STRING_AGG (s_last_name, ', ') 'Author', s_pub_name 'Publisher'
FROM books
LEFT JOIN wrote ON (books.n_book_id = wrote.n_book_id)
LEFT JOIN author ON (wrote.n_author_id = author.n_author_id)
LEFT JOIN publisher ON (books.n_publisher_id = publisher.n_publisher_id)
GROUP BY books.n_book_id, s_pub_name;