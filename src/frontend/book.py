import isbnlib

class Book:

    def __init__(self):
        self.author_first_names = None
        self.author_last_names = None
        self.author_address = None
        self.publisher_name = None
        self.publisher_address = None
        self.book_title = None
        self.book_edition = None
        self.book_language = None
        self.book_genre = None
        self.book_isbn = None
    
    def set(self,   
            author_first_names,
            author_last_names,
            author_address,
            publisher_name,
            publisher_address,
            book_title,
            book_edition,
            book_language,
            book_genre,
            book_isbn):

        self.author_first_names = author_first_names
        self.author_last_names = author_last_names
        self.author_address = author_address
        self.publisher_name = publisher_name
        self.publisher_address = publisher_address
        self.book_title = book_title
        self.book_edition = book_edition
        self.book_language = book_language
        self.book_genre = book_genre
        self.book_isbn = book_isbn

    def get_meta_from_isbn(self, s_isbn="9780062893338"):
        meta_data = isbnlib.meta(s_isbn)

        self.author_first_names = []
        self.author_last_names = []
        for author in meta_data['Authors']:
            name = author.split(" ")
            last_name = name.pop(-1)
            first_names = " ".join(name)
            self.author_first_names.append(last_name)
            self.author_last_names.append(first_names)

        
        self.publisher_name = meta_data["Publisher"]
        self.book_title = meta_data["Title"]
        self.book_language = meta_data["Language"]
        self.book_isbn = list(meta_data.values())[0]

        #print(meta_data)
        
    def __str__(self):
        return(f"""ISBN: {self.book_isbn}
Titel: {self.book_title}
Author First Names: {self.author_first_names}
Author Last Names: {self.author_last_names}
Language: {self.book_language}
Publisher: {self.publisher_name}""")

if __name__ == "__main__":
    my_class = Book()
    isbn = input("ISBN eingeben: ")
    if isbn != str():
        my_class.get_meta_from_isbn(isbn)
        print(my_class)
    else:
        my_class.get_meta_from_isbn()
        print(my_class)