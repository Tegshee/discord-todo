# bot.py
from discord.ext import commands
from collections import defaultdict
import discord

from needhelp.config import EMOJI_NUMBERS
from needhelp.config import INTENTS
from needhelp.additionals import show_todo
from needhelp import logging as log

from models import User, Todo, Task, Category


# create test code bot.py here
# create main function

if __name__ == "__main__":
    # from bot_commands import todo_list
    # guild_id = None
    # user_id = 624791398570524672
    # todos = todo_list(user_id=user_id, guild_id=guild_id)

    # for todo in todos:
    #     log.info(todo.tasks)

    # msg = show_todo(todos)

    from needhelp.additionals import parse_todo_id

    parse_todo_id("""🏠 - 1 - My first todo
        1️⃣ - My first task ✅
        2️⃣ - My second task ⏳
        3️⃣ - My third task ❌
        """
    )
