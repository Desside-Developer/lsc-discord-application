import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
import cogs.database.database as dbMaria

import logging
print = logging.info

# Logs
# Category

class economy_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_balance = dbMaria.get_user_balance(user_id)
        await interaction.response.send_message(f"Your balance is {user_balance}")
        pass
        
"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(economy_system(client))
        print(f"{Fore.GREEN}Cog '{Fore.RED}{economy_system}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}{economy_system}{Fore.GREEN}': {e}{Style.RESET_ALL}")
