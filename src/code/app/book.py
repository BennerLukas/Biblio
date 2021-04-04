import isbnlib


class Book:

    def __init__(self) -> object:
        self.author_first_names = None
        self.author_last_names = None
        self.publisher_name = None
        self.book_title = None
        self.book_edition = 1
        self.book_language = None
        self.book_genre = None
        self.book_isbn = None
        self.publishing_year = None
        self.location_id = None
        self.reco_age = None

    def set_manually(self, param_list):
        if len(param_list) == 10:
            return False

        self.author_first_names = param_list[0]
        self.author_last_names = param_list[1]
        self.publisher_name = param_list[2]
        self.book_title = param_list[3]
        self.book_edition = param_list[4]
        self.book_language = param_list[5]
        self.book_genre = param_list[6]
        self.book_isbn = param_list[7]
        self.publishing_year = param_list[8]
        self.location_id = param_list[9]
        self.reco_age = param_list[10]

    def set_via_isbn(self, s_isbn: str = "9780062893338"):
        # remove "-" from isbn string
        s_isbn = "".join(s_isbn.strip("-"))

        meta_data = isbnlib.meta(s_isbn)
        print(meta_data)

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

        if self.publisher_name == "":
            self.publisher_name = None

    def get_s_sql_call(self) -> str or None:

        if self.book_title is None:
            return None
        # if self.publisher_name is None:
        #     return None
        if self.author_last_names is None:
            return None

        call = f"""CALL add_book(
                        ARRAY{self.author_first_names.split(" ")}, 
                        ARRAY{self.author_last_names.split(" ")},
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