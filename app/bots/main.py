import sys
sys.path.append('/code/app/bots')
sys.path.append('/code/app/bots/handlers')
sys.path.append('/code/app/bots/commands')
sys.path.append('/code/app/bots/tickets')

import discord
import platform
import time
import logging
import asyncio

from colorama import Back, Fore, Style

from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
from dispie import EmbedCreator

from database.database import dbMaria
from config import Bot_tickets, tickets_cogs


class CustomLogging():
    logger: logging
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
    def log(self, message):
        self.logger.info(message)
print = CustomLogging().log

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
        self.cogslist = [
            "logs.logging",
            "commands.system_start",
            "commands.database_system",
            "tickets.ticket_report",
            "tickets.ticket_rent",
            "tickets.ticket_cheap",
            "tickets.ticket_rep",
            "tickets.ticket_set"
            ]
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)
    async def on_ready(self):
        try:
            guild = self.get_guild(1200955239281467422)
            await self.tree.sync(guild=guild)
            await self.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='twinsikk', url='https://www.twitch.tv/twinsikk'))
            prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
            print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
            print(prfx + " ID: " + Fore.YELLOW + str(self.user.id))
            print(prfx + " Version: " + Fore.YELLOW + str(discord.__version__))
            print(prfx + " Platform: " + Fore.YELLOW + platform.system())
            print(prfx + " Python: " + Fore.YELLOW + platform.python_version())
            print(prfx + " Discord.py: " + Fore.YELLOW + discord.__version__)
            print(prfx + " Bot: " + Fore.YELLOW + "Bot_tickets")
            print(f"{Fore.GREEN}Бот {self.user} запущен!{Style.RESET_ALL}")
            print(f'Вошёл как {self.user} (ID: {self.user.id})')
            Embed = discord.Embed(title="🚀° Bot Info", description=
            f"""
            ``Bot``: **Запущен**
            ``Logged in as``: **{self.user.name}**
            ``ID``: **{str(self.user.id)}**
            ``Version``: **{str(discord.__version__)}**
            ``Platform``: **{platform.system()}**
            ``Python``: **{platform.python_version()}**
            ``Discord.py``: **{discord.__version__}**
            """, color=0x77eb34)
            Embed.set_thumbnail(url="https://i.imgur.com/J60RRnz.png")
            user = self.get_user(960251916762378241)
            if user:
                await user.send(embed=Embed)
            else:
                logging.error(f"Admin user with ID {960251916762378241} not found.")
        except Exception as e:
            print(f"{Fore.RED}Error logging in as {self.user}: {e}{Style.RESET_ALL}")

Client = Client()
# Command's next
"""
Slash Commands Next: //
help
"""

@Client.tree.command(name="test-garage", description="embed")
async def embed(interaction: discord.Interaction):
    embed_main = discord.Embed(color=0xffffff, title="📌‧ нᴀɯи ᴦᴀᴩᴀжи!", description=f"""Если у вас возникают вопросы.
- Обратитесь к модераторам
- или к администраторам. ↙
- <#1205649863937761370>
        """
        )
    embed_main.set_image(url="https://i.imgur.com/sOyS2oX.png")
    embed_main.set_footer(text="**𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨**  [✅]")
    embed_info = discord.Embed(color=0xffffff, title="📌‧ зᴀᴋᴧᴀдᴋᴀ", description=f"""
Спасибо за ваше сотрудничество!
""")
    await interaction.channel.send(embed=embed_main)
    await interaction.channel.send(embed=embed_info)
    await interaction.response.send_message("Ready", ephemeral=True)

@Client.event
async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(1214952893271248946)
    background = Editor('app/bots/Reports-banner.png')
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((150, 150)).circle_image()
    popping = Font.poppins(size=50, variant="bold")
    poppins_small = Font.poppins(size=20, variant="light")
    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, outline=None, stroke_width=5)
    background.text((450, 160), member.name, color="white", font=popping)
    background.text((450, 200), str(member.id), color="white", font=poppins_small)  # Convert member.id to string
    file = File(fp=background.image_bytes, filename="https://i.imgur.com/8txHSse.png")
    await channel.send(file=file)
    try:
        channel = member.guild.get_channel(1207710865202221076)
        if channel:
            await channel.send(f'```Индентификатор:{member.id}``` ```Имя пользователя:{member.name}``` ```Присоединился:{member.joined_at}``` Аватар:{member.avatar}!')
            role = member.guild.get_role(1204254987396448287)
            if role:
                await member.add_roles(role)
                print(f'Участнику {member.name} присвоена роль {role.name}.')
            else:
                print('Указанная роль не найдена.')
        else:
            print('Указанный канал не найден.')
    except Exception as e:
        print(f'Ошибка при обработке события on_member_join: {e}')
@Client.event
async def message_event(member: discord.Member):
    try:
        channel = member.guild.get_channel(1207710865202221076)
        if channel:
            await channel.send(f'```Индентификатор:{member.id}``` ```Имя пользователя:{member.name}``` ```Присоединился:{member.joined_at}``` Аватар:{member.avatar}!')
            role = member.guild.get_role(1204254987396448287)
            if role:
                await member.add_roles(role)
                print(f'Участнику {member.name} присвоена роль {role.name}.')
            else:
                print('Указанная роль не найдена.')
        else:
            print('Указанный канал не найден.')
    except Exception as e: discord.message



"""Start Client"""
Client.run(Bot_tickets)