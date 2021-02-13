INSERT INTO ADDRESSES (s_street, s_house_number, s_city, s_country, n_zipcode)
VALUES
('Hauptstraße', 54, 'Mannheim', 'Germany', 68165),
('Bahnhofstraße', 23, 'Mannheim', 'Germany', 68165),
('Gartenweg', 12, 'Stuttgart', 'Germany', 70173),
('Wall Street', 1235, 'New York', 'USA', 10005);

INSERT INTO AUTHOR(s_first_name, s_last_name, n_address_id)
VALUES
('Aaronovitch', 'Ben', 1),
('Abawi', 'Atia', 2),
('Abel', 'Susanne', 3);

INSERT INTO PUBLISHER(s_pub_name, n_address_id)
VALUES
('Heyne Verlag', 4),
('Akademische Arbeitsgemeinschaft Verlag', 1),
('Andiamo Verlag', 2);

INSERT INTO LIB_LOCATION (s_compartment, s_shelf, s_room, n_loc_floor, n_address_id)
VALUES
('2B', '3', '203', 1, 2),
(NULL, 'A', 'Lesezimmer', 8, 1),
('A', '15', '104', 1, 2);

INSERT INTO BOOKS(s_isbn, s_title, n_book_edition, s_genre, dt_publishing_date, s_book_language, n_recommended_age, b_is_availalbe, n_publisher_id, n_location_id)
VALUES
('9780575097568', 'Rivers of London', 1, 'Urban Fantasy', DATE '2011-01-10', 'en', NULL, true, 1, 2), -- Author 1
('9780345524591', 'Moon Over Soho', 2, 'Urban Fantasy', DATE '2011-04-21', NULL , NULL, true, 1, 2),  -- Author 1
('9780525516019', 'A Land of Permanent Goodbyes', NULL, NULL, NULL, 'en', 18, true, 1, 1), -- Author 3
(NULL, 'Der Text des Lebens', NULL, NULL, NULL, 'de', 40, true, 2, 3); -- Author 2 

INSERT INTO USERS(s_first_name, s_last_name, dt_date_of_birth, n_address_id)
VALUES
('Ben', 'Hell',  DATE '1987-04-03', 3),
('Nadia', 'Tall',  DATE '1968-10-31', 4),
('Susanne', 'Nieble',  DATE'2001-02-25', NULL);

INSERT INTO LOAN (ts_now, n_user_id)
VALUES
('2020-11-28 12:12:12', 1),
('2020-12-28 14:23:51', 2),
('2021-01-28 08:56:22', 3);

INSERT INTO BORROW_ITEM (n_duration, n_book_id, n_loan_id, b_active)
VALUES
(14, 1, 2, false),
(7, 3, 2, false),
(7, 2, 1, false),
(21, 4, 3, false);

INSERT INTO READ_BOOKS(n_book_id, n_user_id)
VALUES
(1, 2),
(3, 2),
(2, 1),
(4, 3);

INSERT INTO WROTE(n_book_id, n_author_id)
VALUES
(1, 1),
(2, 1),
(2, 3),
(3, 3),
(4, 2);

