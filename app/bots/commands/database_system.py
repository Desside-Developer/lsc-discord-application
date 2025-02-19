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
    @app_commands.command(name="sync", description="the commands")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction: discord.Interaction):
        await self.client.tree.sync(guild=interaction.guild)
        await interaction.response.send_message("Synced", ephemeral=True)
    @app_commands.command(name="database-execute", description="1324234")
    @app_commands.checks.has_permissions(administrator=True)
    async def database_execute(self, interaction: discord.Interaction, *, subfolder: str):
        if not self.check_user_is_owner(interaction.user.id):
            await interaction.response.send_message("У вас нет прав на выполнение данной команды!", ephemeral=True)
        try:
            dbMaria.execute_all_sql_files_in_subfolder(subfolder)
            await interaction.response.send_message("Запрос отправлен!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Ошибка при отправке запросов: {e}", ephemeral=True)
    async def check_user_is_owner(self, user_id: int) -> bool:
        return user_id == config.owner_id

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [database_system]
    for cog in cogs:
        try:
            await client.add_cog(cog(client), guilds=[discord.Object(id=1200955239281467422)])
            print(f"{Fore.GREEN}Cog '{Fore.RED}database_system{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}database_system{Fore.GREEN}': {e}{Style.RESET_ALL}")
