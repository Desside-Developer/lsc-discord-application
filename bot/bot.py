# from __init__ import *
import asyncio
import discord
from discord.ext import commands, ipc
from discord.ext.ipc import Server
from discord.ext.ipc.objects import ClientPayload
from config import BOT_TOKEN, COGS_LIST

import uvicorn
import logging
print=logging.error

class application(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix=self.get_prefix, intents=discord.Intents.all())
    if not hasattr(self, "ipc"):
      self.ipc = ipc.Server(self, host="0.0.0.0", secret_key="test01")
    self.prefixes={}
# Setup Cogs
  async def setup_hook(self):
    for ext in COGS_LIST:
      await self.load_extension(ext)
# Ready Bot
  async def on_ready(self):
    await self.change_presence(status=discord.Status.dnd, activity=discord.Game("@Not Working"))
    await self.ipc.start()
# Prefix System >>>
  # async def get_prefix(self,message):
  #   guild_id = message.guild.id if message.guild else None
  #   prefix = rRedis.getPrefixes(guild_id)
  #   if prefix:Z
  #       return cm.when_mentioned_or(prefix.decode())(self, message)
  #   else:
  #       return '!'  # Default prefix if not found in Redis

  # async def load_prefixes_from_db(self):
  #   try:
  #     data = dbMaria.get_all_data('guild_configuration')
  #     for entry in data:
  #         try:
  #           guild_id = int(entry['guild_id'])  # Ensure guild_id is an integer
  #           prefix = entry['prefix']
  #           rRedis.savePrefixesToHash(guild_id, prefix)
  #           print(f"Loaded prefix '{prefix}' for guild {guild_id}")
  #         except (ValueError, KeyError) as e:
  #           print(f"Error loading guild configuration: {e}")
  #   except Exception as e:
  #     print(f"Error fetching data from database: {e}")

  @Server.route()
  async def get_user_data(self, data: ClientPayload) -> dict:
    user = self.get_user(data.user_id)
    return user._to_minimal_user_json()

  @Server.route()
  async def get_guilds(self, _):
    return str(len(self.guilds))

  async def on_ipc_error(self, endpoint: str, exc: Exception) -> None:
    raise exc

# Status Activity 

  # async def load_status_activity(self,status:str) -> None:
  #   await self.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='twinsikk', url='https://www.twitch.tv/twinsikk'))
  #   await self.change_presence(status=discord.Status.online, activity=discord.Game(name='Dota 2'))
  #   await self.change_presence(status=discord.Status.invisible)
  #   await self.change_presence(status=discord.Status.offline)
  #   await self.change_presence(status=discord.Status.do_not_disturb)
    
  #   raise NotImplementedError('i don\' create')


# Disconect Application ( Don't Working )







"""Start Client"""
if __name__ == "__main__":
  client_bot = application()
  client_bot.run(BOT_TOKEN, reconnect=False)