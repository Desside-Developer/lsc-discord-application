import datetime
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from fastapi import APIRouter, HTTPException
from discord.ui import View, Button
from database.database import dbMaria
from database.redis import rRedis
import config 
import logging
from unicodedata import category
import asyncio

router = APIRouter()
router.tags = ["Configuration [API]"]

class configuration(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client


@router.post(path='/config/set/{guild_Id}/{prefix_new}')
async def changePrefix(guild_id, prefix_new):
    try:
        prefix = rRedis.getPrefixes(guild_id)
        if prefix:
            dbMaria.update_data(table_name='guild_configuration', new_data={'prefix': prefix_new}, condition_column='guild_id', condition_value=guild_id)
            rRedis.savePrefixesToHash(guild_id, prefix_new)
            return HTTPException(200, f'Successfully! Prefix replace <{prefix}> . <{prefix_new}>')
        return HTTPException(200, 'Not Found! Prefix in redis not found.')
    except Exception as e:
        raise HTTPException(500, f'Error: {e}')

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(configuration(client))
        print(f"{Fore.GREEN}Configuration '{Fore.RED}Config{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding config '{Fore.RED}Config{Fore.GREEN}': {e}{Style.RESET_ALL}")
