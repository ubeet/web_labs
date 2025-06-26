from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, crud
from database import SessionLocal, engine
import psycopg2

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/docs")
templates = Jinja2Templates(directory="html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request, role: str = "user", db: Session = Depends(get_db)):
    news = crud.get_news(db)
    categories = db.query(models.Category).all()
    users = db.query(models.User).all()
    return templates.TemplateResponse("index.html", {
        "request": request, "news": news, "categories": categories, "users": users, "role": role
    })

@app.post("/add")
def add_news(title: str = Form(...), content: str = Form(...), category_id: int = Form(...),
             user_id: int = Form(...), db: Session = Depends(get_db)):
    crud.create_news(db, title, content, category_id, user_id)
    return RedirectResponse("/?role=admin", status_code=303)

@app.get("/delete/{news_id}")
def delete_news(news_id: int, db: Session = Depends(get_db)):
    crud.delete_news(db, news_id)
    return RedirectResponse("/?role=admin", status_code=303)

@app.get("/news/{news_id}", response_class=HTMLResponse)
def view_news(news_id: int, request: Request, role: str = "user", db: Session = Depends(get_db)):
    news = crud.get_news_by_id(db, news_id)
    categories = db.query(models.Category).all()
    users = db.query(models.User).all()
    return templates.TemplateResponse("news_detail.html", {
        "request": request, "news": news, "categories": categories, "users": users, "role": role
    })

@app.post("/news/{news_id}")
def update_news(news_id: int, title: str = Form(...), content: str = Form(...),
                category_id: int = Form(...), user_id: int = Form(...),
                db: Session = Depends(get_db)):
    crud.update_news(db, news_id, title, content, category_id, user_id)
    return RedirectResponse(f"/?role=admin", status_code=303)

@app.get("/stats")
def get_news_count():
    conn = psycopg2.connect("dbname=newsdb user=postgres password=pass host=localhost port=5433")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM news")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"news_count": count}

@app.get("/category_select", response_class=HTMLResponse)
def category_form(request: Request, db: Session = Depends(get_db), role: str = "user"):
    categories = db.query(models.Category).all()
    return templates.TemplateResponse("category_select.html", {
        "request": request,
        "categories": categories,
        "role": role,
        "news": None,
        "selected_category": None
    })


@app.post("/category_select", response_class=HTMLResponse)
def show_selected_category(request: Request, category_id: int = Form(...), db: Session = Depends(get_db), role: str = "user"):
    categories = db.query(models.Category).all()
    selected = db.query(models.Category).get(category_id)
    news = db.query(models.News).filter(models.News.category_id == category_id).all()
    return templates.TemplateResponse("category_select.html", {
        "request": request,
        "categories": categories,
        "news": news,
        "role": role,
        "selected_category": selected
    })

