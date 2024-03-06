import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
import cogs.database.database as dbMaria

import logging
print = logging.info

# Logs
# Category

class music_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="играть-музыку", description="нет информации")
    async def play(self, interaction: discord.Interaction, url: str):
        await interaction.response.send_message("Музыка играется!")
        pass
    @app_commands.command(name="пауза", description="нет информации")
    async def pause(self, interaction: discord.Interaction):
        await interaction.response.send_message("Музыка пауза!")
        pass
    @app_commands.command(name="продолжить", description="нет информации")
    async def resume(self, interaction: discord.Interaction):
        await interaction.response.send_message("Музыка продолжается!")
        pass
    @app_commands.command(name="перемотка", description="нет информации")
    async def skip(self, interaction: discord.Interaction):
        await interaction.response.send_message("Музыка перемотана!")
        pass
    @app_commands.command(name="очистить-плейлист", description="нет информации")
    async def clear(self, interaction: discord.Interaction):
        await interaction.response.send_message("Музыка очищена!")
        pass
    @app_commands.command(name="показать-плейлист", description="нет информации")
    async def show(self, interaction: discord.Interaction):
        await interaction.response.send_message("Музыка показана!")
        pass
    @app_commands.command(name="выключить-бота", description="нет информации")
    async def shutdown(self, interaction: discord.Interaction):
        await interaction.response.send_message("Бот выключен!")
        pass
    @app_commands.command(name="помощь", description="нет информации")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message("Музыка помощь!")
        pass
        
        
        
        
        
"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(music_system(client))
        print(f"{Fore.GREEN}Cog '{Fore.RED}{music_system}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}{music_system}{Fore.GREEN}': {e}{Style.RESET_ALL}")
