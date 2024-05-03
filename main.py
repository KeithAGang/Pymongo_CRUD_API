from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from database import collection, book_collection
from random import randint
from schemas import *
from models import *
from library import *
from sorting import *
from searching import *

app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost:5173",
    "http://localhost:5001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/")
async def get_all_todos():
    data = collection.find()
    return all_data(data)

@router.post("/")
async def create_task(new_task: Todo):
    try:
        resp = collection.insert_one(dict(new_task))
        return {
            "status_code": 200,
            "id": str(resp.inserted_id)
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured: {e}")
    
@router.post("/add_book")
async def add_book(new_book: Book):
    try:
        resp = book_collection.insert_one(dict(new_book))
        return "Success"
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured: {e}")
        
@router.get("/library")
async def fill_lib():

    fill_library(book_collection)
    
    books = book_collection.find()
    if (books == [""]):
        return {"message": "No Books Found!"}
    else:
        return all_books(books)
    
@router.post("/sort")
async def sort_data(sort_details: Sort):
    sort_details = dict(sort_details)
    sorting_algorithms = {
        "bubble sort": bubble_sort,
        "selection sort": selection_sort,
        "merge sort": merge_sort,
        "insertion sort": insertion_sort,
        "quick sort": quick_sort,
    }
    
    if (sort_details["algorithm"] not in sorting_algorithms):
        return f"Enter A Valid Sorting Algorithm Like: {list(sorting_algorithms.keys())}"
    
  
        
    books = list(book_collection.find())
    response = sorting_algorithms[sort_details["algorithm"]](books, param=sort_details["sort_by"], order=sort_details["order"])
    
    
    return {
        "algorithm": sort_details["algorithm"],
        "Sort order": sort_details["order"],
        "Filter": sort_details["sort_by"],
        "Complexities": response["complexities"],  
        "items": len(all_books(response["data"])),  
        "Data": all_books(response["data"])
    }
    
@router.post("/search")
async def search_data(search_details: Search):
    search_details = dict(search_details)
    data = list(book_collection.find())
    
    sorting_algorithms = [
        bubble_sort,
        selection_sort,
        merge_sort,
        insertion_sort,
        quick_sort
    ]
    
    searching_algorithms = {
        "linear search": linear_search,
        "binary search": binary_search,
        "hash table search": hash_table_search,
        "jump search": jump_search,
        "interpolation search": interpolation_search
    }
    
    num = randint(0,4)
    
    if (search_details["algorithm"] not in searching_algorithms):
        return f"Please Enter A Valid Sorting Algorith like: {list(searching_algorithms.keys())}"
    
    if ((search_details["search_by"] == "id") | (search_details["search_by"] == "publication_year")):
        search_details["search_value"] = int(search_details["search_value"])
    
    sorted_data = sorting_algorithms[num](data, param=search_details["search_by"])
    
    response = searching_algorithms[search_details["algorithm"]](list(sorted_data["data"]), search_details["search_value"], param=search_details["search_by"])
    
    if (not response):
        return {"data": "No Books Found"}
    
    return {
        "algorithm": search_details["algorithm"],
        "results": len(response),
        "Data": all_books(response)
        }
    # return list(response)
        

app.include_router(router)