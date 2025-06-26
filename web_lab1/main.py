from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    if not db.query(models.Category).first():
        db.add_all([
            models.Category(name="Технології"),
            models.Category(name="Культура"),
            models.Category(name="Освіта")
        ])
        db.commit()

with SessionLocal() as db:
    if not db.query(models.User).first():
        db.add_all([
            models.User(id=1, username="admin", role="admin"),
            models.User(id=2, username="editor", role="user"),
            models.User(id=3, username="alex", role="user")
        ])
        db.commit()


app = FastAPI(
    title="ІС Новини",
    description="Лаба 1",
    version="0.1",
    docs_url="/swagger"
)

templates = Jinja2Templates(directory="html")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    db: Session = Depends(get_db),
    role: str = "user"
):
    news = crud.get_all_news(db)
    categories = crud.get_all_categories(db)
    users = db.query(models.User).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "news": news,
        "categories": categories,
        "users": users,
        "role": role
    })


@app.get("/news/{news_id}", response_class=HTMLResponse)
def view_news(
    news_id: int,
    request: Request,
    db: Session = Depends(get_db),
    role: str = "user"
):
    news = crud.get_news(db, news_id)
    categories = crud.get_all_categories(db)
    users = db.query(models.User).all()
    return templates.TemplateResponse("news_detail.html", {
        "request": request,
        "news": news,
        "categories": categories,
        "users": users,
        "role": role
    })


@app.post("/news/{news_id}")
def update_news(
    news_id: int,
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    crud.update_news(db, news_id, title, content, category_id, user_id)
    return RedirectResponse("/?role=admin", status_code=303)


@app.get("/delete/{news_id}")
def delete(
    news_id: int,
    db: Session = Depends(get_db)
):
    crud.delete_news(db, news_id)
    return RedirectResponse("/?role=admin", status_code=303)

@app.post("/add")
def add_news(
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    crud.create_news(db, title, content, category_id, user_id)
    return RedirectResponse("/?role=admin", status_code=303)


