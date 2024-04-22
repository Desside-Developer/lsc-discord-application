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

class auto_reload_cogs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @commands.command(name="start-cog/embeds_responder")
    @commands.has_permissions(administrator=True)
    async def nickname_on_join(self, ctx: commands.Context):
        await ctx.message.delete()
        await ctx.send("Нажмите на кнопку ниже, чтобы начать работу с меню.")
        view = View()
        button = Button(label="Начать работу", style=discord.ButtonStyle.green)
        button.callback = self.button_callback
        view.add_item(button)
        await ctx.send("Нажмите на кнопку ниже, чтобы начать работу с меню.", view=view)
"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(auto_reload_cogs(client), guilds=[discord.Object(id=1200955239281467422)])
        print(f"{Fore.GREEN}Cog '{Fore.RED}auto_reload_cogs{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}auto_reload_cogs{Fore.GREEN}': {e}{Style.RESET_ALL}")
