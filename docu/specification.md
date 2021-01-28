# Database specification for 'Biblio'

'Biblio' will be a webapp for organizing your private book collection.

Group-member: Alina Buss (4163246), Phillip Lange (5920414), Lukas Benner (6550912)

The used database schema und functionalities are described in the following:

- Books: Every book is stored in the database with following attributes: title, ISBN, recommended Age, language, publishing date, genre, edition, wether its available and a unique Identifier.

- Author & Publisher: Every Book has a authoter and Publishier assigned. These contain information like address, name and a unique identifier.
- Location: Every book has a location assigned, where its supossed to be. The Location has the following attributes: address, floor, room, shelf, compartment and a unique identifier.
- User: Every user of the database has a name, a user_id and his/her date of birth is stored.
- Borrow: A User can lend severall books. For every loan the timestamp will be stored. For every borrowed item the duration and the Book_ID will be used to assign it to a loan.
- The database can tracks which books a particular user already read.
- The Address is handled in a seperate table and has the following attributes: city, country, street, house number, zipcode and a unique identifier.
