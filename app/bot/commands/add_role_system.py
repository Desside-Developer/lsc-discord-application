import datetime
import os
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria
from handlers.hand_package import save_ticket_for_table, generate_ticket_token, check_user
import config
import logging
print = logging.info

class template(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [template]
    for cog in cogs:
        try:
            await client.add_cog(cog(client))
            print(f"{Fore.GREEN}Cog '{Fore.RED}Adding Role System{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}Adding Role System{Fore.GREEN}': {e}{Style.RESET_ALL}")
