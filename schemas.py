def individual_data(todo):
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "status": todo["is_completed"]
    }

def all_data(todos):
    return [individual_data(todo) for todo in todos]

def individual_book(book):
    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["title"],
        "publication_year": book["publication_year"],
        "genre": book["genre"],
        "description": book["description"]
    }

def all_books(books):
    return [individual_book(book) for book in books]