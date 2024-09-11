import discord
from discord.ext import commands

from database import CategoryManager, TasksManager

tm = TasksManager()


class TaskCreate(discord.ui.Modal, title="Create"):
    task_name = discord.ui.TextInput(label="Name", placeholder="task_name", required=True)
    caregory_id = discord.ui.TextInput(label="Category id", placeholder="caregory_id", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        tm.create_task(self.task_name.value, self.caregory_id.value, 0, interaction.user.id)
        await interaction.response.send_message(f"Created a task **{self.task_name.value}**!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"Oops! Something went wrong.\n{error}", ephemeral=True)


class TaskStatusChange(discord.ui.Modal, title="Delete"):
    task_id = discord.ui.TextInput(label="Name", placeholder="task_id", required=True)
    new_status = discord.ui.TextInput(label="New status", placeholder="new_status", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        tm.set_status(self.task_id.value, self.new_status.value)
        await interaction.response.send_message(f"Done!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"Oops! Something went wrong.\n{error}", ephemeral=True)


class TaskDelete(discord.ui.Modal, title="Delete"):
    task_id = discord.ui.TextInput(label="Name", placeholder="task_id", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        tm.delete_task(self.task_id.value)
        await interaction.response.send_message(f"Deleted a task with id **{self.task_id.value}**!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"Oops! Something went wrong.\n{error}", ephemeral=True)


class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Create", style=discord.ButtonStyle.green)
    async def button_callback1(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(TaskCreate())

    @discord.ui.button(label="Change status", style=discord.ButtonStyle.primary)
    async def button_callback2(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(TaskStatusChange())

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def button_callback3(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(TaskDelete())


@commands.command()
async def task(ctx):
    """Create, delete and change status for tasks."""
    await ctx.send("Please, choose an action.", view=Buttons())


@commands.command()
async def tasks(ctx):
    """Get info about all the tasks, categories and their ids."""
    category_manager = CategoryManager()
    tasks_manager = TasksManager()

    categories = category_manager.get_all_user_categories(ctx.message.author.id)

    embed = discord.Embed(title="Categories and Tasks", color=discord.Color.blue())

    for category in categories:
        category_id = category[0]
        category_name = category[1]
        tasks = tasks_manager.get_tasks_by_category(category_id, ctx.message.author.id)

        task_list = "\n".join([f"{task[1]} - {'✅' if task[2] == 1 else '❌'} (id: {task[0]})" for task in tasks])

        if task_list:
            embed.add_field(
                name=f"{category_name} (id: {category_id})",
                value=task_list,
                inline=False,
            )
        else:
            embed.add_field(
                name=f"{category_name} (id: {category_id})",
                value="No tasks",
                inline=False,
            )

    await ctx.send(embed=embed)
