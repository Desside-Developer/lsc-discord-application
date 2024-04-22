# import datetime
# import discord
# import json
# import logging
# import config 
# from discord.ext import commands
# from colorama import Back, Fore, Style
# from discord import app_commands, utils
# from discord.ui import View, Button
# from database.database import dbMaria

# print = logging.info

# class on_member_logs(commands.Cog):
#     def __init__(self, client: commands.Bot):
#         self.client = client
#     @commands.Cog.listener()

# """
# - Setup Cogs ->
# """
# async def setup(client: commands.Bot) -> None:
#     cogs = [on_member_logs]
#     for cog in cogs:
#         try:
#             await client.add_cog(cog(client))
#             print(f"{Fore.GREEN}Cog '{Fore.RED}{cog}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
#         except Exception as e:
#             print(f"{Fore.RED}Error adding cog '{Fore.RED}{cog}{Fore.GREEN}': {e}{Style.RESET_ALL}")
