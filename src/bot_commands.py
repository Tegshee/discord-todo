from db import get_db_session
from models import Todo, Task, Category, User
from sqlalchemy.orm import joinedload

from needhelp import logging as log
from needhelp.additionals import show_todo

# create a global session
session = next(get_db_session())

def add_todo(data):

    user = session.query(User).filter(User.discord_id == data['user_id']).first()
    log.info(f"User: {user}")


    # EMOJI_CATEGORIES = {
    #     'work': '💼',
    #     'private': '🏠',
    #     'school': '🏫',
    #     "party": "🎉",
    #     "travel": "🛫",
    #     "food": "🍔",
    #     "health": "🏥"
    # }
    if data['todo_type'] == 'channel':
        category_id = 1
        
    else:
        category_id = 2 #private
    
    if user is None:
        user = User(
            name=data['created_by'],
            discord_id=data['user_id']
        )
        # save user to db
        session.add(user)


    # create todo 
    todo = Todo(
        title=data['title'],
        message_id=data['message_id'],
        user_id=data['user_id'],
        channel_id=data['channel_id'],
        guild_id=data['guild_id'],
        todo_type=data['todo_type'],
        created_by=data['created_by'],
        category_id=category_id,
    )
    # get todo id after commit 
    session.add(todo)
    session.commit()

    # create task
    task = Task(
        title='All done!',
        todo_id=todo.id,
        created_by=user.name,
        emoji_count=0,
    )

    # add task to session
    
    session.add(task)
    session.commit()

    return todo


def todo_list(user_id, guild_id):
    if guild_id:
        #todos with category name emoji 
        todos = session.query(Todo).options(joinedload(Todo.tasks), joinedload(Todo.category)).filter(Todo.todo_type == 'channel').filter(Todo.guild_id == guild_id).all()
    else:
        todos = session.query(Todo).options(joinedload(Todo.tasks), joinedload(Todo.category)).filter(Todo.todo_type == 'private').filter(Todo.user_id == user_id).all()
    
    return todos


def task_status_change(todo_id, task_position, up_vote=True):
    log.info(f"task_position: {task_position}")
    log.info(f"todo_id: {todo_id}")
    todo = session.query(Todo).filter(Todo.id == todo_id).first()
    count = 1
    for task in todo.tasks:
        if task_position == count:
            if up_vote:
                task.emoji_count += 1
            elif task.emoji_count > 0:
                task.emoji_count -= 1
            
            if up_vote:
                task.status = 'done'
            else:
                task.status = 'in_progress'
            session.add(task)
            session.commit()
            return True
        count += 1
    else:
        return None
    

def get_todo_msg_by_id(todo_id):
    todo = session.query(Todo).options(joinedload(Todo.tasks), joinedload(Todo.category)).filter(Todo.id == todo_id).first()
    msg = show_todo(todo)
    return msg


def get_todo_by_id(todo_id):
    todo = session.query(Todo).filter(Todo.id == todo_id).first()
    return todo


def add_task(todo_id, title, author):
    todo = session.query(Todo).filter(Todo.id == todo_id).first()
    task = Task(
        title=title,
        todo_id=todo.id,
        created_by=author,
        emoji_count=0,
    )
    session.add(task)
    session.commit()
    return task