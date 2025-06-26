from app import app, db
from models import Category
with app.app_context():
    db.create_all()
    db.session.add(Category(name='Технології'))
    db.session.add(Category(name='Політика'))
    db.session.commit()
