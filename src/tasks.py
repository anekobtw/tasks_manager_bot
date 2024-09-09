import discord
from discord.ext import commands

from database import CategoryManager, TasksManager

tm = TasksManager()


@commands.command()
async def task(ctx, action: str, arg: str | int, *args):
    if action == "create":
        tm.create_task(" ".join(args), arg, 0)
        embed = discord.Embed(title=f"Created a task {' '.join(args)}", color=discord.Color.green())
        embed.set_footer(text="© anekobtw, 2024")
        await ctx.send(embed=embed)

    elif action == "set_status":
        tm.set_status(arg, args[0])
        embed = discord.Embed(title=f"Done!", color=discord.Color.green())
        embed.set_footer(text="© anekobtw, 2024")
        await ctx.send(embed=embed)

    elif action == "delete":
        name = tm.find_task(arg)[1]
        tm.delete_task(task_id=arg)
        embed = discord.Embed(title=f"Deleted a task {name}", color=discord.Color.red())
        embed.set_footer(text="© anekobtw, 2024")
        await ctx.send(embed=embed)


@commands.command()
async def tasks(ctx):
    category_manager = CategoryManager()
    tasks_manager = TasksManager()

    categories = category_manager.get_all_categories()

    embed = discord.Embed(title="Categories and Tasks", color=discord.Color.blue())

    for category in categories:
        category_id = category[0]
        category_name = category[1]
        tasks = tasks_manager.get_tasks_by_category(category_id)

        task_list = "\n".join([f"{task[1]} - {'✅' if task[2] == 1 else '❌'} (id: {task[0]})" for task in tasks])

        if task_list:
            embed.add_field(name=f"{category_name} (id: {category_id})", value=task_list, inline=False)
        else:
            embed.add_field(name=f"{category_name} (id: {category_id})", value="No tasks", inline=False)

    await ctx.send(embed=embed)
