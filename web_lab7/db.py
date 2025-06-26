from app import db
from models import Category, User
from werkzeug.security import generate_password_hash
from app import app

with app.app_context():
    db.create_all()
    db.session.add(Category(name="Технології"))
    db.session.add(Category(name="Політика"))
    db.session.add(User(username="admin", password=generate_password_hash("pass"), is_admin=True))
    db.session.commit()
