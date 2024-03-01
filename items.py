import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="tigotov", description="modal windows up")
    async def modal(self, interaction: discord.Interaction):
        await interaction.response.send_message("modal windows up")


"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(Help(client))
        print(f"{Fore.GREEN}Cog '{Fore.RED}{Help}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}{Help}{Fore.GREEN}': {e}{Style.RESET_ALL}")