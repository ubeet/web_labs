from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from bson import ObjectId, errors
from mongo_db import news_col, users_col, categories_col

app = FastAPI(title="Лаба 3 - FastAPI + MongoDB")
templates = Jinja2Templates(directory="html")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, role: str = "user"):
    news = list(news_col.find())

    for n in news:
        n["id"] = str(n["_id"])
        try:
            n["category"] = categories_col.find_one({"_id": ObjectId(n["category_id"])})
        except:
            n["category"] = None
        try:
            n["user"] = users_col.find_one({"_id": ObjectId(n["user_id"])})
        except:
            n["user"] = None

    return templates.TemplateResponse("index.html", {
        "request": request,
        "news": news,
        "role": role,
        "categories": list(categories_col.find()),
        "users": list(users_col.find())
    })

@app.post("/add")
def add_news(title: str = Form(...), content: str = Form(...), category_id: str = Form(...), user_id: str = Form(...)):
    news_col.insert_one({
        "title": title,
        "content": content,
        "category_id": category_id,
        "user_id": user_id
    })
    return RedirectResponse("/?role=admin", status_code=303)

@app.get("/news/{news_id}", response_class=HTMLResponse)
def news_detail(news_id: str, request: Request, role: str = "user"):
    news = news_col.find_one({"_id": ObjectId(news_id)})
    if not news:
        return RedirectResponse("/")
    news["id"] = str(news["_id"])
    news["category"] = categories_col.find_one({"_id": ObjectId(news["category_id"])})
    news["user"] = users_col.find_one({"_id": ObjectId(news["user_id"])})

    return templates.TemplateResponse("news_detail.html", {
        "request": request,
        "news": news,
        "categories": list(categories_col.find()),
        "users": list(users_col.find()),
        "role": role
    })

@app.post("/news/{news_id}")
def update_news(news_id: str, title: str = Form(...), content: str = Form(...), category_id: str = Form(...), user_id: str = Form(...)):
    news_col.update_one(
        {"_id": ObjectId(news_id)},
        {"$set": {
            "title": title,
            "content": content,
            "category_id": category_id,
            "user_id": user_id
        }}
    )
    return RedirectResponse("/?role=admin", status_code=303)

@app.get("/delete/{news_id}")
def delete_news(news_id: str):
    news_col.delete_one({"_id": ObjectId(news_id)})
    return RedirectResponse("/?role=admin", status_code=303)
