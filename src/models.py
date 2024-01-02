# models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import datetime

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    message_id = Column(String, default=None)
    title = Column(String)
    tasks = relationship('Task', backref='todo')
    #category relation with one to one
    category = relationship('Category', backref='todo')
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(String, default=None)
    channel_id = Column(String, default=None)
    guild_id = Column(String, default=None)
    todo_type = Column(Enum('private', 'channel', 'global'))
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    todo_id = Column(Integer, ForeignKey('todo.id'))
    status = Column(Enum('todo', 'done', 'in_progress'))
    emoji_count = Column(Integer, default=0)
    # add created_by default is null and created_at updated_at deleted_at
    created_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    emoji = Column(String)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    discord_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    def __repr__(self):
        return f"<User(name={self.name}, id={self.id})>"
    
    def add_user(self):
        pass


class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    discord_id = Column(String)
    guild_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
