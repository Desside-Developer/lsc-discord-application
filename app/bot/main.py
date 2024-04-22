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
import uvicorn

from colorama import Back, Fore, Style

from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
from dispie import EmbedCreator

from database.database import dbMaria
from config import Bot_tickets, tickets_cogs, cogslist
from database.redis import rRedis
# manager_redis = redis.StrictRedis(host='bot-redis-stack-1', port=6379, db=0)

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
        super().__init__(command_prefix=self.get_prefix, intents=discord.Intents.all())
        self.prefixes = {}
    # async def get_prefix(self, message):
    #     guild_id = message.guild.id if message.guild else None
    #     return commands.when_mentioned_or(self.prefixes.get(guild_id, '!'))(self, message)
    async def get_prefix(self, message):
        guild_id = message.guild.id if message.guild else None
        # prefix = manager_redis.get(f'prefix:{guild_id}')  # Get prefix from Redis
        # prefix = manager_redis.hget('guild_prefixes', guild_id)
        prefix = rRedis.getPrefixes(guild_id)
        if prefix:
            return commands.when_mentioned_or(prefix.decode())(self, message)
        else:
            return '!'  # Default prefix if not found in Redis
    async def setup_hook(self):
        for ext in cogslist:
            await self.load_extension(ext)
    async def on_ready(self):
        try:
            await client.load_prefixes_from_db()
            guild = self.get_guild(1200955239281467422)
            await self.tree.sync(guild=guild)
            await self.tree.sync()
            await self.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='twinsikk', url='https://www.twitch.tv/twinsikk'))
            prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
            logging.info(f"""{Fore.CYAN}Logged in as: {Fore.LIGHTGREEN_EX}{self.user.name}
{Fore.CYAN}Id: {Fore.LIGHTGREEN_EX}{self.user.id}
{Fore.CYAN}Version: {Fore.LIGHTGREEN_EX}{discord.__version__}
{Fore.CYAN}Platform: {Fore.LIGHTGREEN_EX}{platform.system()}
{Fore.CYAN}Python: {Fore.LIGHTGREEN_EX}{platform.python_version()}
{Fore.CYAN}Discord.py: {Fore.LIGHTGREEN_EX}{discord.__version__}
{Fore.LIGHTYELLOW_EX}Bot: {Fore.MAGENTA}``{self.user}`` Start! {Style.RESET_ALL}""")
            Embed = discord.Embed(title="🚀° Bot Info", description=
            f"""``Bot``: **{self.user}**
            ``Logged in as``: **{self.user.name}**
            ``ID``: **{str(self.user.id)}**
            ``Version``: **{str(discord.__version__)}**
            ``Platform``: **{platform.system()}**
            ``Python``: **{platform.python_version()}**
            ``Discord.py``: **{discord.__version__}**""", color=0xFF8716)
            Embed.set_thumbnail(url="https://i.imgur.com/J60RRnz.png")
            user = self.get_user(960251916762378241)
            if user:
                return await user.send(embed=Embed)
            logging.error(f"Admin user with ID {960251916762378241} not found.")
        except Exception as e:
            print(f"{Fore.RED}Error logging in as {self.user}: {e}{Style.RESET_ALL}")
    async def load_prefixes_from_db(self):
        try:
            data = dbMaria.get_all_data('guild_configuration')
            for entry in data:
                try:
                    guild_id = int(entry['guild_id'])  # Ensure guild_id is an integer
                    prefix = entry['prefix']
                    # self.prefixes[guild_id] = prefix
                    # manager_redis.set(f'prefix:{guild_id}', prefix)
                    # manager_redis.hset('guild_prefixes', guild_id, prefix)
                    rRedis.savePrefixesToHash(guild_id, prefix)
                    print(f"Loaded prefix '{prefix}' for guild {guild_id}")
                except (ValueError, KeyError) as e:
                    print(f"Error loading guild configuration: {e}")
        except Exception as e:
            print(f"Error fetching data from database: {e}")
    async def on_disconnect(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Бот был отключен в {current_time}')

client_bot = Client()
# Command's next
"""
Slash Commands Next: //
help
"""

# Command Load Extension
async def load_extension():
    Client.load_extension()
# Command Unload Extension
# Command Reload Extension

@client_bot.command(name="embed_responder")
@commands.has_permissions(administrator=True)
async def admin_embed(ctx: commands.Context):
    await ctx.message.delete()
    view = EmbedCreator(bot=Client)
    await ctx.send(embed=view.get_default_embed, view=view)


@client_bot.command(name="clearslash", description="Clears all registered slash commands.")
@commands.is_owner()
async def clearslash(ctx: commands.Context):
    """Clears all registered slash commands. Only the bot owner can use this command."""
    await ctx.reply("Clearing all slash commands...", mention_author=False)
    guild_id = 1200955239281467422
    Client.tree.clear_commands(guild=discord.Object(id=guild_id))
    await ctx.reply("All slash commands have been cleared.", mention_author=False)

@client_bot.command(name='deletecommands', aliases=['clear'])
@commands.is_owner()
async def delete_commands(ctx):
    Client.tree.clear_commands(guild=None)
    await Client.tree.sync()
    await ctx.send('Commands deleted.')


@client_bot.command(name='test-garage')
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


"""Start Client"""
if __name__ == "__main__":
    client = Client()
    client.run(Bot_tickets)