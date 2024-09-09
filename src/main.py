import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from category import category
from help import help
from tasks import task, tasks

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
bot.remove_command("help")

bot.add_command(category)
bot.add_command(task)
bot.add_command(tasks)
bot.add_command(help)

load_dotenv()
bot.run(os.getenv("TOKEN"))
