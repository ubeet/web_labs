from mongo_db import users_col, categories_col

if users_col.count_documents({}) == 0:
    users_col.insert_many([
        {"username": "admin"},
        {"username": "editor"},
        {"username": "alex"}
    ])

if categories_col.count_documents({}) == 0:
    categories_col.insert_many([
        {"name": "Технології"},
        {"name": "Культура"},
        {"name": "Освіта"}
    ])
