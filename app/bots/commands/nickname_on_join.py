import datetime
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.app_commands import AllChannels
from discord.ext import commands
from discord.ui import View, Button
from app.bots.database.database import dbMaria
import config 
import logging
from unicodedata import category
import asyncio


class test(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="treeees", description="@everyone System Nickames on join")
    async def nickname_on_join(self, interaction: discord.Interaction):
        await interaction.response.send_message("System Nicknames on join")

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(test(client), guilds=[discord.Object(id=1200955239281467422)])
        print(f"{Fore.GREEN}Cog '{Fore.RED}{test}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}{test}{Fore.GREEN}': {e}{Style.RESET_ALL}")
