import discord
from discord.ext import commands

from database import CategoryManager

cm = CategoryManager()


class CategoryCreate(discord.ui.Modal, title="Create"):
    name = discord.ui.TextInput(label="Name", placeholder="category_name", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        cm.create_category(category_name=self.name.value)
        await interaction.response.send_message(f"Created a category **{self.name.value}**!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"Oops! Something went wrong.\n{error}", ephemeral=True)


class CategoryDelete(discord.ui.Modal, title="Delete"):
    category_id = discord.ui.TextInput(label="Id", placeholder="category_id", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        cm.delete_category(category_id=self.category_id.value)
        await interaction.response.send_message(f"Deleted a category with id **{self.category_id.value}**!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f"Oops! Something went wrong.\n{error}", ephemeral=True)


class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Create", style=discord.ButtonStyle.green)
    async def button_callback1(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(CategoryCreate())

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def button_callback2(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(CategoryDelete())


@commands.command()
async def category(ctx):
    """Create and delete categories."""
    await ctx.send("Please, choose an action.", view=Buttons())
