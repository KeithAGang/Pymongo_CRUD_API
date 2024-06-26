from pymongo.mongo_client import MongoClient
from pymongo import DESCENDING
import os

DATABASE_URL= os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)

db = client["algorithms"]
collection = db["todo_data"]
book_collection = db["library"]