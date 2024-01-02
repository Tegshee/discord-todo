# bot.py
from discord.ext import commands
from collections import defaultdict
import discord

from needhelp.config import EMOJI_NUMBERS
from needhelp.config import INTENTS
from needhelp.additionals import show_todo
from needhelp.additionals import parse_todo_id
from needhelp import logging as log

from bot_commands import add_todo, todo_list
from bot_commands import task_status_change
from bot_commands import get_todo_msg_by_id
from bot_commands import get_todo_by_id
from bot_commands import add_task

from models import User


# client = discord.Client(intents=intents)
guild = discord.Guild
bot = commands.Bot(command_prefix='!', intents=INTENTS) 


@bot.command(name='todo')
async def todo(ctx, command, *, task=None):
    if command == 'add' and task is not None:
        
        log.info(f"todo message: {ctx.message}")
        #check ctx.message.guild is not None
        if ctx.message.guild is not None:
            guild_id = ctx.message.guild.id
            todo_type = 'channel'
        else:
            guild_id = None
            todo_type = 'private'
            
        #create todo
        todo = add_todo({
            'title': task,
            'message_id': ctx.message.id,
            'user_id': ctx.message.author.id,
            'channel_id': ctx.message.channel.id,
            'guild_id': guild_id,
            'todo_type': todo_type,
            'created_by': ctx.message.author.name,
        })
        # return added task end reaction to the message

        msg = show_todo(todo)

        message = await ctx.send(msg)
        await message.add_reaction(EMOJI_NUMBERS[1])

            
    elif command == 'list':
        #get all todos for the user
        log.info(f"todo message: {ctx.message}")
        #check ctx.message.guild is not None
        # check if guild is not None
        if ctx.message.guild is not None:
            guild_id = ctx.message.guild.id
        else:
            guild_id = None

        log.error(f"guild_id: {guild_id}")
        todos = todo_list(ctx.message.author.id, guild_id=guild_id)

        for todo in todos:
            log.info(todo)
            msg = show_todo(todo)
            if todo.category.name == 'work':
                message = await ctx.send(msg) 
            else:
                user = await bot.fetch_user(ctx.message.author.id)
                message = await user.send(msg)
            
            task_count = 1
            for task in todo.tasks:
                await message.add_reaction(EMOJI_NUMBERS[task_count])
                task_count += 1

    # elif command == 'done' and task is not None:
    #     if task in todo_list:
    #         todo_list.remove(task)
    #         await ctx.send(f'Task removed: {task}')
    #     else:
    #         await ctx.send('Task not found.')

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return  # Ignore reactions from bots

    log.info(reaction)
    log.info(reaction.message.id)
    # log.info(reaction_counts[reaction.message.id])

    todo_id = parse_todo_id(reaction.message.content)
    if todo_id is None:
        return
    
    #check emoji in EMOJI_NUMBERS dict and add the number emoji
    if reaction.emoji in EMOJI_NUMBERS.values():
        emoji_location = list(EMOJI_NUMBERS.keys())[list(EMOJI_NUMBERS.values()).index(reaction.emoji)]

        #count the reaction.emoji of message 
        log.info(reaction.emoji)
        log.info("-----------------")

        task_status_change(todo_id, emoji_location, up_vote=True)

        todo = get_todo_msg_by_id(todo_id)

        await reaction.message.edit(content=f'{todo}')
        
@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return  # Ignore reactions from bots
    if user.bot:
        return  # Ignore reactions from bots

    log.info(reaction)
    log.info(reaction.message.id)
    # log.info(reaction_counts[reaction.message.id])

    todo_id = parse_todo_id(reaction.message.content)
    if todo_id is None:
        return
    
    #check emoji in EMOJI_NUMBERS dict and add the number emoji
    if reaction.emoji in EMOJI_NUMBERS.values():
        emoji_location = list(EMOJI_NUMBERS.keys())[list(EMOJI_NUMBERS.values()).index(reaction.emoji)]

        task_status_change(todo_id, emoji_location, up_vote=False)
        todo = get_todo_msg_by_id(todo_id)
        await reaction.message.edit(content=f'{todo}')


@bot.event
async def on_message(message):
    if message.reference is not None:
        # This is a reply
        user = await bot.fetch_user(message.author.id)

        replied_to = await message.channel.fetch_message(message.reference.message_id)
        # print(f"{message.author} replied to {replied_to.author}'s message: {replied_to.content}")
        todo_id = parse_todo_id(replied_to.content)
        if todo_id is None:
            return
        
        # check replied_to.content is start with task string
        # if yes then add task to the todo
        # else add todo to the todo
        if message.content.startswith('task'):
            # add task to the todo
            # add_task(todo_id, message.content, message.author.name)
            add_task(todo_id, message.content.replace('task', ''), user.name)
            msg = get_todo_msg_by_id(todo_id)
            # sent new message 
            new_message = await message.channel.send(f'{msg}')
            todo = get_todo_by_id(todo_id)
            
            task_count = 1
            for task in todo.tasks:
                await new_message.add_reaction(EMOJI_NUMBERS[task_count])
                task_count += 1
        else:
            # add todo to the todo
            return
        
    await bot.process_commands(message)
