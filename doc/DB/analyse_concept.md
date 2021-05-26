# Analyse to perform 3NF

1. atomar attributes

- There are only Single Valued Attributes.
- Attribute Domain does not change.
- There is a Unique name for every Attribute/Column.
- The order in which data is stored, does not matter.

    Therfore we did following:
    - split address
    - split names
    - allowed several author
    - unique names inside a table

2. remove the repeated information

- Second Normal Form (2NF) is based on the concept of full functional dependency.

    Therfore we did following:
    - delete address attributes
    - make seperat address table

3. No non-primary-key attribute is transitively dependent on the primary key

- A relation is in third normal form, if there is no transitive dependency for non-prime attributes as well as it is in second normal form.

    Therefore we did following:
    - made seperate tables for author, publisher and connected it with the books table
