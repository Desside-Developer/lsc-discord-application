import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria
# from cogs.service.check_role import check_user_on_owner
import config 
import logging
print = logging.info

class database_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @commands.command(name="sync")
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx: commands.Context):
        await self.client.tree.sync(guild=ctx.guild)
        await ctx.send("Synced")

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(database_system(client), guilds=[discord.Object(id=1200955239281467422)])
        print(f"{Fore.GREEN}Cog '{Fore.RED}database_system{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}database_system{Fore.GREEN}': {e}{Style.RESET_ALL}")
