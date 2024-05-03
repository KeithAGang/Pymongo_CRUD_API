from pydantic import BaseModel
from datetime import datetime

class Todo(BaseModel):
    title: str
    description: str
    is_completed: bool = False
    is_deleted: bool = False
    creation: int = int(datetime.timestamp(datetime.now()))
    updated: int = int(datetime.timestamp(datetime.now()))
    
    
class Book(BaseModel):
    title: str
    Year: int
    description: str
    
class Sort(BaseModel):
    algorithm: str
    order: str = "asc"
    sort_by: str   
    
class Search(BaseModel):
    algorithm: str
    search_by: str
    search_value: str
   