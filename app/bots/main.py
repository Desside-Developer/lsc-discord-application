import sys
sys.path.append('/code/app/bots')
sys.path.append('/code/app/bots/handlers')
sys.path.append('/code/app/bots/commands')
sys.path.append('/code/app/bots/events')
sys.path.append('/code/app/bots/tickets')

import redis
import discord
import platform
import time
import logging
import asyncio
import datetime

from colorama import Back, Fore, Style

from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
from dispie import EmbedCreator

from database.database import dbMaria
from config import Bot_tickets, tickets_cogs
manager_redis = redis.StrictRedis(host='bot-redis-stack-1', port=6379, db=0)

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
        super().__init__(command_prefix=commands.when_mentioned_or('%'), intents=discord.Intents.all())
        self.cogslist = [
            "logs.logging",
            "commands.system_start",
            "commands.system_on_reaction",
            "commands.database_system",
            "commands.nickname_on_join",
            "commands.embeds_responder",
            "commands.auto_reload_cogs",
            "commands.status_server",
            "events.on_member",
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
            await self.tree.sync()
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
@Client.command(name="embed_responder")
@commands.has_permissions(administrator=True)
async def admin_embed(ctx: commands.Context):
    await ctx.message.delete()
    view = EmbedCreator(bot=Client)
    await ctx.send(embed=view.get_default_embed, view=view)


@Client.command(name="clearslash", description="Clears all registered slash commands.")
@commands.is_owner()
async def clearslash(ctx: commands.Context):
    """Clears all registered slash commands. Only the bot owner can use this command."""
    await ctx.reply("Clearing all slash commands...", mention_author=False)
    guild_id = 1200955239281467422
    Client.tree.clear_commands(guild=discord.Object(id=guild_id))
    await ctx.reply("All slash commands have been cleared.", mention_author=False)

@Client.command(name='deletecommands', aliases=['clear'])
@commands.is_owner()
async def delete_commands(ctx):
    Client.tree.clear_commands(guild=None)
    await Client.tree.sync()
    await ctx.send('Commands deleted.')


@Client.command(name='test-garage')
@commands.is_owner()
async def embed(ctx: commands.Context):
    embed_main = discord.Embed(color=0xffffff, title="📌‧ нᴀɯи ᴦᴀᴩᴀжи!", description=f"""Если у вас возникают вопросы.
- Обратитесь к модераторам
- или к администраторам. ↙
- <#1205649863937761370>
        """
        )
    embed_main.set_image(url="https://i.imgur.com/sOyS2oX.png")
    embed_main.set_footer(text="**𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨**  [✅]")
    embed_info = discord.Embed(color=0x63f700, title="📌‧ зᴀᴋᴧᴀдᴋᴀ", description=f"""
Спасибо за ваше сотрудничество!
""")
    await ctx.send(embed=embed_main)
    await ctx.send(embed=embed_info)

@Client.event
async def on_disconnect():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'Бот был отключен в {current_time}')

"""Start Client"""
if __name__ == "__main__":
    Client.run(Bot_tickets)
    