import isbnlib


class Book:

    def __init__(self):
        self.author_first_names = None
        self.author_last_names = None
        self.publisher_name = None
        self.book_title = None
        self.book_edition = None
        self.book_language = None
        self.book_genre = None
        self.book_isbn = None
        self.publishing_year = None
        self.location_id = None
        self.reco_age = None

    def set_manually(self,
                     author_first_names=None,
                     author_last_names=None,
                     publisher_name=None,
                     book_title=None,
                     book_edition=None,
                     book_language=None,
                     book_genre=None,
                     book_isbn=None,
                     publishing_year=None,
                     location_id=None,
                     reco_age=None
                     ):

        self.author_first_names = author_first_names
        self.author_last_names = author_last_names
        self.publisher_name = publisher_name
        self.book_title = book_title
        self.book_edition = book_edition
        self.book_language = book_language
        self.book_genre = book_genre
        self.book_isbn = book_isbn
        self.publishing_year = publishing_year
        self.location_id = location_id
        self.reco_age = reco_age

    def set_via_isbn(self, s_isbn: str = "9780062893338"):
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
        self.publishing_year = meta_data['Year']
        self.book_isbn = list(meta_data.values())[0]

        # print(meta_data)

    def get_s_sql_call(self) -> str or None:

        if self.book_title is None:
            return None
        if self.publisher_name is None:
            return None
        if self.author_last_names is None:
            return None

        call = f"""CALL add_book(
                        ARRAY{self.author_first_names}, 
                        ARRAY{self.author_last_names},
                        {self.publishing_year}, 
                        '{self.publisher_name}',
                        '{self.book_title}', 
                        {self.book_edition},
                        '{self.book_language}', 
                        '{self.book_genre}', 
                        '{self.book_isbn}', 
                        {self.location_id},
                        {self.reco_age});"""

        call = call.replace("'None'", "NULL").replace("None", "NULL")
        print(call)
        return call

    def __str__(self):
        return (f"""ISBN: {self.book_isbn}
                Titel: {self.book_title}
                Author First Names: {self.author_first_names}
                Author Last Names: {self.author_last_names}
                Language: {self.book_language}
                Publisher: {self.publisher_name}""")