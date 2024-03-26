import os
import discord
import logging

from discord.ext import commands
from colorama import Back, Fore, Style

print = logging.info

class logs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    async def auth_users(self, dict):
        Embed = discord.Embed(title="🚀° Auth_Response", description=
        f"""
        ``user_id``: **{dict['user_id']}**
        ``unique_id``: **{dict['unique_id']}**
        ``username``: **{dict['username']}**
        ``balance``: **{dict['balance']}**
        ``on_joined``: **{dict['on_joined']}**
        ``inventory``: **{dict['inventory']}**
        """, color=0xffffff)
        Embed.set_thumbnail(url="https://i.imgur.com/J60RRnz.png")
        admin_user = self.client.get_user(960251916762378241)
        if admin_user:
            await admin_user.send(embed=Embed)
        else:
            logging.error(f"Admin user with ID {960251916762378241} not found.")

logs_responde = None

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    global logs_responde
    try:
        logs_responde = logs(client)
        await client.add_cog(logs(client), guilds=[discord.Object(id=1200955239281467422)])
        print(f"{Fore.GREEN}Cog '{Fore.RED}logs{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}logs{Fore.GREEN}': {e}{Style.RESET_ALL}")
