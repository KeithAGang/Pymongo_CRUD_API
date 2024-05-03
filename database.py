from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL= os.getenv('DATABASE_URL')

client = MongoClient(DATABASE_URL)

db = client["algorithms"]
collection = db["todo_data"]
book_collection = db["library"]