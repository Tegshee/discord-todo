from sqlalchemy.orm import Session
from models import Category, User, Base
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine('sqlite:///database.db')  # replace with your actual database URL
Base.metadata.bind = engine
DBSession = Session(bind=engine)

def seed_categories():
    EMOJI_CATEGORIES = {
        'work': '💼',
        'private': '🏠',
        'school': '🏫',
        "party": "🎉", 
        "travel": "🛫",
        "food": "🍔",
        "health": "🏥"
    }

    for category_name, emoji in EMOJI_CATEGORIES.items():
        category = Category(name=category_name, emoji=emoji)
        DBSession.add(category)

    DBSession.commit()

if __name__ == "__main__":
    seed_categories()