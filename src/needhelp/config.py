import os

import discord

from dotenv import load_dotenv
load_dotenv()

INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
INTENTS.reactions = True
INTENTS.members = True

EMOJI_NUMBERS = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    10: "🔟"
}

EMOJI_CATEGORIES = {
    'work': '💼',
    'private': '🏠',
    'school': '🏫',
    "party": "🎉", 
    "travel": "🛫",
    "food": "🍔",
    "health": "🏥"
}

TOKEN = os.getenv('DISCORD_TOKEN')
