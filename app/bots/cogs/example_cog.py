from discord.ext import commands
import discord

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say_hello")
    async def say_hello(self, ctx):
        """Отвечает приветствием."""
        await ctx.send("Привет! Я пример расширения.")

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
    # Регистрация слэш-команды
    @bot.tree.command(name="hello_slash", description="Приветствие через слэш-команду")
    async def hello_slash(interaction: discord.Interaction):
        await interaction.response.send_message("Привет! Я пример слэш-команды в расширении.")
