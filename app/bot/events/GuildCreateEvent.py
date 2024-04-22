import datetime
import discord
import json
import logging
import config 
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria
from database.redis import rRedis

# manager_redis = redis.StrictRedis(host='bot-redis-stack-1', port=6379, db=0)
print = logging.info

class GuildEventJoin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        data = dbMaria.get_data_by_condition(table_name='guild_configuration',condition_column='guild_id',condition_value=guild.id)
        if data:
            return print(f'This Guild {guild.id} in database')
        # manager_redis.hset('guild_prefixes', guild.id, '?')
        rRedis.savePrefixesToHash(guild.id, '?')
        dbMaria.insert_data(table_name='guild_configuration', data={"guild_id": guild.id})
        return print(f"Guild '{guild.name}' ({guild.id}) added to the database.")

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(GuildEventJoin(client))
        print(f"{Fore.LIGHTBLUE_EX}Event '{Fore.LIGHTMAGENTA_EX}GuildEventJoin{Fore.LIGHTBLUE_EX}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding event '{Fore.RED}GuildEventJoin{Fore.GREEN}': {e}{Style.RESET_ALL}")
