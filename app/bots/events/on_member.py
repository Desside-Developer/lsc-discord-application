import datetime
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria
import config 
import logging
from unicodedata import category
import asyncio

print = logging.info

class on_member_logs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.get_channel(1214952893271248946)
        if channel:
            Embed = discord.Embed(title="Зашёл на наш сервер !!!", color=0xffffff, description=f"""
⚜️⇢ **Индентификатор**: ``{member.id}``

🪪⇢ **Упоминалка пользователя**: {member.mention}

🔑⇢ **Присоединился**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
""")
            Embed.set_thumbnail(url=member.avatar)
            Embed.set_image(url="https://i.imgur.com/38rEjs8.png") 
            await channel.send(embed=Embed)
        else:
            print('Указанный канал для логирования не найден.')
        logging.info(f"{member.name} ({member.id}) присоединился к серверу.")
        # role = member.guild.get_role(1204254987396448287)
        # if role:
        #     await member.add_roles(role)
        #     print(f'Участнику {member.name} присвоена роль {role.name}.')
        # else:
        #     print('Указанная роль не найдена.')
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = member.guild.get_channel(1214952893271248946)
        if channel:
            Embed = discord.Embed(title="Ушёл с нашего сервера :(", color=0xffffff, description=f"""
⚜️⇢ **Индентификатор**: ``{member.id}``

🪪⇢ **Упоминалка пользователя**: {member.mention}

⛔️⇢ **Ушёл от нас**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
""")
            Embed.set_thumbnail(url=member.avatar)
            Embed.set_image(url="https://i.imgur.com/38rEjs8.png")
            dbMaria.delete_one_data('tags_users', 'user_id', member.id)
            dbMaria.delete_one_data('assigned_tickets', 'user_id', member.id)
            dbMaria.delete_one_data('tickets', 'user_id', member.id)
            dbMaria.delete_one_data('users', 'user_id', member.id)
            await channel.send(embed=Embed)
        else:
            print('Указанный канал для логирования не найден.')
        logging.info(f"{member.name} ({member.id}) покинул сервер.")


"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [on_member_logs]
    for cog in cogs:
        try:
            await client.add_cog(cog(client))
            print(f"{Fore.GREEN}Cog '{Fore.RED}{cog}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}{cog}{Fore.GREEN}': {e}{Style.RESET_ALL}")
