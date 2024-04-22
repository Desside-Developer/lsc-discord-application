import os
import json
import logging
import discord
import datetime
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button, Select
from database.database import dbMaria
from handlers.hand_package import save_ticket_for_table, generate_ticket_token, check_user
import config

print = logging.info

class ticket(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client





"""
- Setup Cogs ->
"""

async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(ticket(client))
        print(f"{Fore.GREEN}Cog '{Fore.BLUE}ticket{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.BLUE}ticket{Fore.GREEN}': {e}{Style.RESET_ALL}")
