import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
import cogs.database.database as dbMaria

import logging
print = logging.info


class add_role_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="add-role-system", description="Emoji-Add-Role")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_role_system(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Добавление роли", description="Нажмите на кнопку чтобы добавить роль", color= discord.Colour.blue())
        embed.set_author(name="Gustavs")
        embed.set_footer(text="@ПОчитайте правила!")
        await interaction.channel.send(embed=embed, view=buttons_adding_role())
        await interaction.response.send_message("Система ролей добавлена!", ephemeral=True)
class buttons_adding_role(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="1", style=discord.ButtonStyle.green, custom_id="testW", emoji="🪙")
    async def add_role_first(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = 1204254987396448287
        if interaction.guild.get_role(role) in interaction.user.roles:
            await interaction.response.send_message("У вас уже есть роль!", ephemeral=True)
            return
        else:
            await interaction.response.send_message("Роль добавлена!", ephemeral=True)
            await interaction.user.add_roles(interaction.guild.get_role(role))
    @discord.ui.button(label="2", style=discord.ButtonStyle.green, custom_id="testQ", emoji="🎁")
    async def add_role_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = 1204254984581939251
        if interaction.guild.get_role(role) in interaction.user.roles:
            await interaction.response.send_message("У вас уже есть роль!", ephemeral=True)
            return
        else:
            await interaction.response.send_message("Роль добавлена!", ephemeral=True)
            await interaction.user.add_roles(interaction.guild.get_role(role))
    @discord.ui.button(label="Get info", style=discord.ButtonStyle.grey, custom_id="testE") 
    async def url(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.label = "Открыто!"
        button.disabled = True
        await interaction.response.send_message("Открыто!", ephemeral=True)

"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [add_role_system]
    for cog in cogs:
        try:
            client.add_view(buttons_adding_role())
            await client.add_cog(cog(client))
            print(f"{Fore.GREEN}Cog '{Fore.RED}{cog}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}{cog}{Fore.GREEN}': {e}{Style.RESET_ALL}")
            continue
