from datetime import datetime
from books2 import books2

def fill_library(book_collection):
    # Insert each list item into the database
    for book in books2:
        # Convert negative publication years (representing BCE) to positive
        if book["publication_year"] < 0:
            book["publication_year"] = abs(book["publication_year"])
            # Create a datetime object for BCE years
            book["published_year"] = datetime(year=book["publication_year"], month=1, day=1)
        else:
            # Create a datetime object for AD years
            book["published_year"] = datetime(year=book["publication_year"], month=1, day=1)
        book_collection.insert_one(book)

# Example usage
# Assuming you have a MongoDB collection named "my_books"
# fill_library(my_books)
