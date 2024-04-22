import datetime
import discord
import json
import logging
import config 
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria

print = logging.info

class MessageCreate(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @commands.Cog.listener()
    async def on_message(self, guild: discord.Guild):
        pass

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(MessageCreate(client))
        print(f"{Fore.LIGHTBLUE_EX}Event '{Fore.LIGHTMAGENTA_EX}MessageCreate{Fore.LIGHTBLUE_EX}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding event '{Fore.RED}MessageCreate{Fore.GREEN}': {e}{Style.RESET_ALL}")
