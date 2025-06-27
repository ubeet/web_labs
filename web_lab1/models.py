from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    role = Column(String)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class News(Base):
    __tablename__ = "news"
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category")
