-- 1. The first query selects all basic information to all books, as i.e. author, title, ISBN, Location, Publisher... . 
-- The second query represents the collection of the basic information for a particular book.

SELECT b.s_isbn             AS ISBN,
       b.s_title            AS Booktitle,
       b.n_book_edition     AS Bookedition,
       b.s_genre            AS Bookgenre,
       b.n_publishing_year  AS Publishingdate,
       b.s_book_language    AS Booklenguage,
       b.n_recommended_age  AS Recommended_Age,
       b.b_is_available     AS Availabilty,
       au.s_first_name      AS Author_first_name,
       au.s_last_name       AS Author_last_name,
       l.s_compartment      AS Location_compartment,
       l.s_shelf            AS Location_shelf,
       l.s_room             AS Location_room,
       l.n_loc_floor        AS Location_floor,
       ad.s_street          AS Location_street,
       ad.s_house_number    AS Location_house_number,
       ad.s_city            AS Location_city,
       ad.s_country         AS Location_country,
       ad.n_zipcode         AS Location_zipcode,
       pu.s_pub_name        AS Publisher
FROM books AS b
         LEFT JOIN wrote AS w ON b.n_book_id = w.n_book_id
         LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
         LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
         LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
         LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id;


SELECT b.s_isbn             AS ISBN,
       b.s_title            AS Booktitle,
       b.n_book_edition     AS Bookedition,
       b.s_genre            AS Bookgenre,
       b.n_publishing_year AS Publishingdate,
       b.s_book_language    AS Booklenguage,
       b.n_recommended_age  AS Recommended_Age,
       b.b_is_available     AS Availabilty,
       au.s_first_name      AS Author_first_name,
       au.s_last_name       AS Author_last_name,
       l.s_compartment      AS Location_compartment,
       l.s_shelf            AS Location_shelf,
       l.s_room             AS Location_room,
       l.n_loc_floor        AS Location_floor,
       ad.s_street          AS Location_street,
       ad.s_house_number    AS Location_house_number,
       ad.s_city            AS Location_city,
       ad.s_country         AS Location_country,
       ad.n_zipcode         AS Location_zipcode,
       pu.s_pub_name        AS Publisher
FROM books AS b
         LEFT JOIN wrote AS w ON b.n_book_id = w.n_book_id
         LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
         LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
         LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
         LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id
WHERE b.n_book_id = '1';

-- 2.The first query select all information about the loan history of all user, as i.e. Username, Loan_ID, timestamp, duration and borrowed items.
-- The second query represents the loan history for a particular users.

SELECT u.s_first_name    AS User_first_name,
       u.s_last_name     AS User_last_name,
       l.n_loan_id       AS Loan_id,
       l.ts_now          AS Loan_timestamp,
       bi.n_duration     AS Loan_duration,
       bi.b_active       AS Loan_active,
       bo.s_isbn         AS Book_ISBN,
       bo.s_title        AS Book_title,
       bo.n_book_edition AS Book_edition
FROM users AS u
         LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
         LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
         LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id;


SELECT u.s_first_name    AS User_first_name,
       u.s_last_name     AS User_last_name,
       l.n_loan_id       AS Loan_id,
       l.ts_now          AS Loan_timestamp,
       bi.n_duration     AS Loan_duration,
       bi.b_active       AS Loan_active,
       bo.s_isbn         AS Book_ISBN,
       bo.s_title        AS Book_title,
       bo.n_book_edition AS Book_edition
FROM users AS u
         LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
         LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
         LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
WHERE u.n_user_id = '1';

-- 3. The first query selects the active loans of all users concatenated with the necessary information about the loans and corresponding user.
-- The second query shows the active loans of one particular user.

SELECT u.s_first_name    AS User_first_name,
       u.s_last_name     AS User_last_name,
       l.n_loan_id       AS Loan_id,
       l.ts_now          AS Loan_timestamp,
       bi.n_duration     AS Loan_duration,
       bi.b_active       AS Loan_active,
       bo.s_isbn         AS Book_ISBN,
       bo.s_title        AS Book_title,
       bo.n_book_edition AS Book_edition
FROM users AS u
         LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
         LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
         LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
WHERE bi.b_active = 'true';

SELECT u.s_first_name    AS User_first_name,
       u.s_last_name     AS User_last_name,
       l.n_loan_id       AS Loan_id,
       l.ts_now          AS Loan_timestamp,
       bi.n_duration     AS Loan_duration,
       bi.b_active       AS Loan_active,
       bo.s_isbn         AS Book_ISBN,
       bo.s_title        AS Book_title,
       bo.n_book_edition AS Book_edition
FROM users AS u
         LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
         LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
         LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
WHERE bi.b_active = 'true'
  and u.n_user_id = '1';

-- 4. The query shows the borrowed items who exceeded there due date. 
-- The due date have been calculated using the timestamp and the duration.

SELECT bi.n_borrow_item_id AS Borrowed_item, bi.n_loan_id AS Loan_id, bi.n_duration + DATE(l.ts_now) AS Due_Date
FROM borrow_item AS bi
         LEFT JOIN loan AS l ON bi.n_loan_id = l.n_loan_id
WHERE CURRENT_DATE > bi.n_duration + DATE(l.ts_now)
  AND bi.b_active = 'TRUE';


-- 5. The query selects the exact location for a particular book with i.e. the address, the floor and the compartment.

SELECT b.s_isbn          AS ISBN,
       b.s_title         AS Booktitle,
       b.n_book_edition  AS Bookedition,
       l.s_compartment   AS Location_compartment,
       l.s_shelf         AS Location_shelf,
       l.s_room          AS Location_room,
       l.n_loc_floor     AS Location_floor,
       ad.s_street       AS Location_street,
       ad.s_house_number AS Location_house_number,
       ad.s_city         AS Location_city,
       ad.s_country      AS Location_country,
       ad.n_zipcode      AS Location_zipcode
FROM books AS b
         LEFT JOIN lib_location AS l ON b.n_location_id = l.n_location_id
         LEFT JOIN addresses AS ad ON l.n_address_id = ad.n_address_id
WHERE b.n_book_id = '1';

-- 6. The queries select all books from a certain genre or language.

SELECT b.s_isbn          AS ISBN,
       b.s_title         AS Booktitle,
       b.n_book_edition  AS Bookedition,
       b.s_genre         AS Book_genre,
       b.s_book_language AS Book_language
FROM books AS b
WHERE b.s_genre = 'Urban Fantasy';

SELECT b.s_isbn          AS ISBN,
       b.s_title         AS Booktitle,
       b.n_book_edition  AS Bookedition,
       b.s_genre         AS Book_genre,
       b.s_book_language AS Book_language
FROM books AS b
WHERE b.s_book_language = 'en';

-- 7. The queries are generating the Count of all books per genre, publisher and author. 

SELECT b.s_genre AS Genre, COUNT(DISTINCT (b.n_book_id)) AS Book_count
FROM books AS b
GROUP BY b.s_genre;

SELECT pu.s_pub_name AS Publisher, COUNT(DISTINCT (b.n_book_id)) AS Book_count
FROM books AS b
         LEFT JOIN publisher AS pu ON b.n_publisher_id = pu.n_publisher_id
GROUP BY pu.s_pub_name;

SELECT au.s_first_name               AS Author_first_name,
       au.s_last_name                AS Author_last_name,
       COUNT(DISTINCT (b.n_book_id)) AS Book_count
FROM books AS b
         LEFT JOIN wrote AS w ON b.n_book_id = w.n_book_id
         LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
GROUP BY au.s_last_name, au.s_first_name;

-- 8. The queries are selecting the 10 most loaned genre, author and publisher per user.

SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP10_genre, rp.count_borrowed_items
FROM (SELECT u.s_first_name             AS User_first_name,
             u.s_last_name              AS User_last_name,
             bo.s_genre                 AS Genre,
             COUNT(bi.n_borrow_item_id) AS Count_borrowed_items,
             rank()
             OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(bi.n_borrow_item_id) DESC)
      FROM users AS u
               LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
               LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
               LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
      GROUP BY u.s_first_name, u.s_last_name, bo.s_genre) AS rp
WHERE rank <= 10;

SELECT rp.user_first_name,
       rp.user_last_name,
       rp.Author_first_name AS TOP10_Author_first_name,
       rp.Author_last_name  AS TOP10_Author_last_name,
       rp.count_borrowed_items
FROM (SELECT u.s_first_name             AS User_first_name,
             u.s_last_name              AS User_last_name,
             au.s_first_name            AS Author_first_name,
             au.s_last_name             AS Author_last_name,
             COUNT(bi.n_borrow_item_id) AS Count_borrowed_items,
             rank()
             OVER (PARTITION BY u.s_first_name, u.s_last_name, au.s_first_name, au.s_last_name ORDER BY COUNT(bi.n_borrow_item_id) DESC)
      FROM users AS u
               LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
               LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
               LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
               LEFT JOIN wrote AS w ON bo.n_book_id = w.n_book_id
               LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
      GROUP BY u.s_first_name, u.s_last_name, au.s_first_name, au.s_last_name) AS rp
WHERE rank <= 10;

SELECT rp.user_first_name, rp.user_last_name, rp.publisher AS TOP10_publisher, rp.count_borrowed_items
FROM (SELECT u.s_first_name             AS User_first_name,
             u.s_last_name              AS User_last_name,
             pu.s_pub_name              AS Publisher,
             COUNT(bi.n_borrow_item_id) AS Count_borrowed_items,
             rank()
             OVER (PARTITION BY u.s_first_name, u.s_last_name, pu.s_pub_name ORDER BY COUNT(bi.n_borrow_item_id) DESC)
      FROM users AS u
               LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
               LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
               LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
               LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
      GROUP BY u.s_first_name, u.s_last_name, pu.s_pub_name) AS rp
WHERE rank <= 10;

-- 9. The queries are counting the total loans per books to determine the most borrowed book.
-- Therfore the 3. and 4. query are only selecting the 10 most borrowed books.
-- Thereby the 2. and 4. query are grouping the results by genre to determine the most borrowed books per genre.

SELECT bo.s_isbn AS Book_ISBN, bo.s_title AS Book_title, COUNT(DISTINCT (bi.n_loan_id)) AS Count_loans
FROM books AS bo
         JOIN borrow_item AS bi ON bo.n_book_id = bi.n_book_id
GROUP BY bo.s_isbn, bo.s_title
ORDER BY COUNT(DISTINCT (bi.n_loan_id)) DESC;

SELECT bo.s_genre                     AS Book_genre,
       bo.s_isbn                      AS Book_ISBN,
       bo.s_title                     AS Book_title,
       COUNT(DISTINCT (bi.n_loan_id)) AS Count_loans
FROM books AS bo
         JOIN borrow_item AS bi ON bo.n_book_id = bi.n_book_id
GROUP BY bo.s_genre, bo.s_isbn, bo.s_title
ORDER BY COUNT(DISTINCT (bi.n_loan_id)) DESC;

SELECT rp.Book_ISBN, rp.Book_title, rp.Count_loans
FROM (SELECT bo.s_isbn                      AS Book_ISBN,
             bo.s_title                     AS Book_title,
             COUNT(DISTINCT (bi.n_loan_id)) AS Count_loans,
             rank() OVER (PARTITION BY bo.s_isbn, bo.s_title ORDER BY COUNT(DISTINCT (bi.n_loan_id)) DESC)
      FROM books AS bo
               JOIN borrow_item AS bi ON bo.n_book_id = bi.n_book_id
      GROUP BY bo.s_isbn, bo.s_title) AS rp
WHERE rank <= 10

SELECT rp.Book_genre, rp.Book_ISBN, rp.Book_title, rp.Count_loans
FROM (SELECT bo.s_genre                     AS Book_genre,
             bo.s_isbn                      AS Book_ISBN,
             bo.s_title                     AS Book_title,
             COUNT(DISTINCT (bi.n_loan_id)) AS Count_loans,
             rank() OVER (PARTITION BY bo.s_genre, bo.s_isbn, bo.s_title ORDER BY COUNT(DISTINCT (bi.n_loan_id)) DESC)
      FROM books AS bo
               JOIN borrow_item AS bi ON bo.n_book_id = bi.n_book_id
      GROUP BY bo.s_genre, bo.s_isbn, bo.s_title) AS rp
WHERE rank <= 10;

-- 10. The query counts the total loans per user.

SELECT u.s_first_name                AS User_first_name,
       u.s_last_name                 AS User_last_name,
       COUNT(DISTINCT (l.n_loan_id)) AS COUNT_Loans
FROM users AS u
         LEFT JOIN loan AS l ON u.n_user_id = l.n_user_id
         LEFT JOIN borrow_item AS bi ON l.n_loan_id = bi.n_loan_id
         LEFT JOIN books AS bo ON bi.n_book_id = bo.n_book_id
GROUP BY u.s_first_name, u.s_last_name;


-- 11. The queries are selecting the 10 most read genre,author and publisher per user.

SELECT rp.user_first_name, rp.user_last_name, rp.genre AS TOP10_genre, rp.count_read_books
FROM (SELECT u.s_first_name           AS User_first_name,
             u.s_last_name            AS User_last_name,
             bo.s_genre               AS Genre,
             COUNT(r.n_read_books_id) AS Count_read_books,
             rank() OVER (PARTITION BY u.s_first_name, u.s_last_name, bo.s_genre ORDER BY COUNT(r.n_read_books_id) DESC)
      FROM users AS u
               LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
               LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
      GROUP BY u.s_first_name, u.s_last_name, bo.s_genre) AS rp
WHERE rank <= 10;


SELECT rp.user_first_name,
       rp.user_last_name,
       rp.Author_first_name AS TOP10_Author_first_name,
       rp.Author_last_name  AS TOP10_Author_last_name,
       rp.count_read_books
FROM (SELECT u.s_first_name           AS User_first_name,
             u.s_last_name            AS User_last_name,
             au.s_first_name          AS Author_first_name,
             au.s_last_name           AS Author_last_name,
             COUNT(r.n_read_books_id) AS Count_read_books,
             rank()
             OVER (PARTITION BY u.s_first_name, u.s_last_name, au.s_first_name, au.s_last_name ORDER BY COUNT(r.n_read_books_id) DESC)
      FROM users AS u
               LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
               LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
               LEFT JOIN wrote AS w ON bo.n_book_id = w.n_book_id
               LEFT JOIN author AS au ON w.n_author_id = au.n_author_id
      GROUP BY u.s_first_name, u.s_last_name, au.s_first_name, au.s_last_name) AS rp
WHERE rank <= 10;

SELECT rp.user_first_name, rp.user_last_name, rp.publisher AS TOP10_publisher, rp.count_read_books
FROM (SELECT u.s_first_name           AS User_first_name,
             u.s_last_name            AS User_last_name,
             pu.s_pub_name            AS Publisher,
             COUNT(r.n_read_books_id) AS Count_read_books,
             rank()
             OVER (PARTITION BY u.s_first_name, u.s_last_name, pu.s_pub_name ORDER BY COUNT(r.n_read_books_id) DESC)
      FROM users AS u
               LEFT JOIN read_books AS r ON u.n_user_id = r.n_user_id
               LEFT JOIN books AS bo ON r.n_book_id = bo.n_book_id
               LEFT JOIN publisher AS pu ON bo.n_publisher_id = pu.n_publisher_id
      GROUP BY u.s_first_name, u.s_last_name, pu.s_pub_name) AS rp
WHERE rank <= 10;