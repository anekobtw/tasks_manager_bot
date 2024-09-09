import discord
from discord.ext import commands


@commands.command()
async def help(ctx):
    description = """
**Categories**
`/category create <category_name>`
`/category delete <category_id>`

**Tasks**
`/task create <category_id> <task_name>`
`/task set_status <task_id> <new_status>`
`/task delete <task_id>`


P.S.
status 0 = incomplete
status 1 = complete
type `/tasks` to get all the ids of categories and tasks
"""
    embed = discord.Embed(title="Commands", description=description, color=0xFF0000)
    embed.set_footer(text="© anekobtw, 2024")
    await ctx.send(embed=embed)
