from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["news_db"]

news_col = db["news"]
categories_col = db["categories"]
users_col = db["users"]
