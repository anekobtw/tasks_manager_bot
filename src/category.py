import discord
from discord.ext import commands

from database import CategoryManager

cm = CategoryManager()


@commands.command()
async def category(ctx, action: str, arg: str):
    if action == "create":
        cm.create_category(category_name=arg)
        embed = discord.Embed(title=f"Created a category {arg}", color=0x00FF40)
        embed.set_footer(text="© anekobtw, 2024")
        await ctx.send(embed=embed)
    elif action == "delete":
        name = cm.find_category(category_id=arg)[1]
        cm.delete_category(category_id=arg)
        embed = discord.Embed(title=f"Deleted a category {name}", color=0xFF0000)
        embed.set_footer(text="© anekobtw, 2024")
        await ctx.send(embed=embed)
