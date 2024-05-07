from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile, Query
from fastapi.staticfiles import StaticFiles
from database import collection, book_collection, DESCENDING
import shutil
from fastapi.middleware.cors import CORSMiddleware 
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
    new_book = dict(new_book)
    try:
        book_data ={
            "id": (book_collection.find_one(sort=[("id", DESCENDING)])["id"] + 1),
            "title": new_book["title"],
            "author": new_book["author"],
            "publication_year": new_book["publication_year"],
            "genre": new_book["genre"],
            "description": new_book["description"]
        }
        resp = book_collection.insert_one(book_data)
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
    
@router.get("/sort")
async def sort_data(
    algorithm: str = Query(..., description="The sorting algorithm to use"),
    order: str = Query(..., description="The desired arrangement order of the data"),
    sort_by: str = Query(..., description="The column to sort the data by")
):
    sorting_algorithms = {
        "bubble sort": bubble_sort,
        "selection sort": selection_sort,
        "merge sort": merge_sort,
        "insertion sort": insertion_sort,
        "quick sort": quick_sort,
    }
    
    if (algorithm not in sorting_algorithms):
        return f"Enter A Valid Sorting Algorithm Like: {list(sorting_algorithms.keys())}"
    
  
        
    books = list(book_collection.find())
    response = sorting_algorithms[algorithm](books, param=sort_by, order=order)
    
    
    return {
        "algorithm": algorithm,
        "Sort order": order,
        "Filter": sort_by,
        "Complexities": response["complexities"],  
        "items": len(all_books(response["data"])),  
        "Data": all_books(response["data"])
    }
    
@router.get("/search")
async def search_data(
    algorithm: str = Query(..., description="The search algorithm to use"),
    search_by: str = Query(..., description="The field to search by"),
    search_value: str = Query(..., description="The value to search for")
):
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
        "interpolation search": interpolation_search,
    }
    
    num = randint(0, 4)
    
    if algorithm not in searching_algorithms:
        return f"Please Enter A Valid Sorting Algorithm like: {list(searching_algorithms.keys())}"
    
    if search_by in ["id", "publication_year"]:
        search_value = int(search_value)
    
    sorted_data = sorting_algorithms[num](data, param=search_by)
    
    response = searching_algorithms[algorithm](list(sorted_data["data"]), search_value, param=search_by)
    
    if not response:
        return {"data": "No Books Found"}
    
    return {
        "algorithm": algorithm,
        "results": len(response),
        "Data": all_books(response)
    }
    
@router.post("/addPic")
async def upload(file: UploadFile = File(...)):
    try:
        last_book_id = book_collection.find_one(sort=[("id", DESCENDING)])["id"]
        
        file.filename = f"{(last_book_id )}.jpg"
        
        with open(f"covers/{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"filename": file.filename}
    except Exception as e:
        print(e)
        return {"message": "There was an error uploading the file"}
        

app.mount("/covers", StaticFiles(directory="covers"), name="covers")

app.include_router(router)