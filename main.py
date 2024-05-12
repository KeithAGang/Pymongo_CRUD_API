import base64
import shutil
import os
from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile, Query, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 
from random import randint

from database import collection, book_collection, DESCENDING
from schemas import *
from models import *
from library import *
from dataPlots import *
from sorting import *
from searching import *

app = FastAPI()
router = APIRouter()

covers_folder = "covers"
if not os.path.exists(covers_folder):
    os.makedirs(covers_folder)

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
            "has_Nobel_Prize": new_book["has_Nobel_Prize"],
            "description": new_book["description"],
        }
        resp = book_collection.insert_one(book_data)
        return "Success"
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured: {e}")
   
@router.get("/books")
async def get_books(
    query: str = Query(..., description="The query parameter")
):
    
    if query == "not_alph":
        query = {'title': {'$not': {'$regex': '^[a-zA-Z]'}}}
        books = book_collection.find(query)
    elif match := re.match(r'^[A-Z]$', query):
        query = {'title': {'$regex': f'^{match.group(0)}'}}
        books = book_collection.find(query)
    else:
        return "Enter a valid query"
    return all_books(books)
    
        
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
        raise HTTPException(status_code=404, detail="No Books Found")
    
    return {
        "algorithm": algorithm,
        "results": len(response),
        "Data": all_books(response)
    }
    
@router.post("/addPic")
async def upload(file: UploadFile = File(...)):
    try:
        last_book_id = book_collection.find_one(sort=[("id", DESCENDING)])["id"]
        file.filename = f"{(last_book_id)}.jpg"
        
        # Check if the 'covers' folder exists, if not, create it
        covers_folder = "covers"
        if not os.path.exists(covers_folder):
            os.makedirs(covers_folder)
        
        with open(os.path.join(covers_folder, file.filename), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {"filename": file.filename}
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The 'covers' folder does not exist and could not be created.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error uploading the file.")
        

@router.get("/plots")
async def data_plots(
    plot: str = Query(..., description="The Plotted Data The User Wants To See.")
):
    
    to_plot = {
        "letters": plot_starting_letters,
        "years":    plot_release_years,
        "nobel_prize": plot_nobel_prize
    }
    
    image = await to_plot[plot](book_collection)
    res_image = base64.b64encode(image.getvalue()).decode('utf-8')
    
    return {
        "plot": plot,
        "image": res_image
    }

@router.delete("/delete")
async def delete_book(
    id: int = Query(..., description="The ID of the Book to Delete.")
):
    result = book_collection.delete_one({"id": id})
    
    
    covers_folder = "/covers"
    
    os.remove(f"{covers_folder}/{id}.jpg")

app.mount("/covers", StaticFiles(directory="covers"), name="covers")

app.include_router(router)