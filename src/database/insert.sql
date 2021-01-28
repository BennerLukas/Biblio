WROTE;
READ_BOOKS;
BORROW_ITEM;
LOAN;
USERS;
BOOKS;


INSERT INTO ADDRESSES (street, house_number, city, country, zipcode)
VALUES
('Hauptstraße', 54, 'Mannheim', 'Germany', 68165),
('Bahnhofstraße', 23, 'Mannheim', 'Germany', 68165),
('Gartenweg', 12, 'Stuttgart', 'Germany', 70173),
('Wall Street', 1235, 'New York', 'USA', 10005);


INSERT INTO PUBLISHER(pub_name, address_id)
VALUES
('Heyne Verlag', 4),
('Akademische Arbeitsgemeinschaft Verlag', 1),
('Andiamo Verlag', 2);

INSERT INTO AUTHOR(first_name, last_name, address_id)
VALUES
('Aaronovitch', 'Ben', 1),
('Abawi', 'Atia', 2),
('Abel', 'Susanne', 3);

INSERT INTO LIB_LOCATION (compartment, shelf, room, loc_floor, address_id)
VALUES
('2B', '3', '203', 1, 2),
(NULL, 'A', 'Lesezimmer', 8, 1),
('A', '15', '104', 1, 2);

INSER INTO BOOKS ()

INSERT INTO USERS(first_name, last_name, date_of_birth, address_id )
VALUES
('Hell', 'Ben', DATE '1987-04-03', 3),
('Tall', 'Nadia', DATE '1968-10-31', 4),
('Nieble', 'Susanne',  DATE'2001-02-25', NULL);

