from books2 import books2

def fill_library(collection):
# Insert each list item into the database
    for book in books2:
        collection.insert_one(book)