import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from category import category
from tasks import task, tasks

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

bot.add_command(category)
bot.add_command(task)
bot.add_command(tasks)

load_dotenv()
bot.run(os.getenv("TOKEN"))
