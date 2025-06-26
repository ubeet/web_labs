from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from database import SessionLocal, engine as pg_engine

sqlite_engine = create_engine("sqlite:///news.db")
SQLiteSession = sessionmaker(bind=sqlite_engine)

models.Base.metadata.create_all(bind=pg_engine)

with SQLiteSession() as old_db, SessionLocal() as new_db:
    for user in old_db.query(models.User).all():
        new_db.merge(models.User(id=user.id, username=user.username, role=user.role))

    for cat in old_db.query(models.Category).all():
        new_db.merge(models.Category(id=cat.id, name=cat.name))

    for n in old_db.query(models.News).all():
        new_db.merge(models.News(
            id=n.id,
            title=n.title,
            content=n.content,
            category_id=n.category_id,
            user_id=n.user_id
        ))

    new_db.commit()

