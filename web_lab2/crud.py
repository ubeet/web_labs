from sqlalchemy.orm import Session
import models

def get_news(db: Session):
    return db.query(models.News).all()

def get_news_by_id(db: Session, news_id: int):
    return db.query(models.News).get(news_id)

def create_news(db: Session, title: str, content: str, category_id: int, user_id: int):
    news = models.News(title=title, content=content, category_id=category_id, user_id=user_id)
    db.add(news)
    db.commit()
    db.refresh(news)
    return news

def update_news(db: Session, news_id: int, title: str, content: str, category_id: int, user_id: int):
    news = db.query(models.News).get(news_id)
    if news:
        news.title = title
        news.content = content
        news.category_id = category_id
        news.user_id = user_id
        db.commit()
        db.refresh(news)
        return news

def delete_news(db: Session, news_id: int):
    news = db.query(models.News).get(news_id)
    if news:
        db.delete(news)
        db.commit()
