import discord
from discord import app_commands, utils, HTTPException
from discord.ext import commands as cm
from discord.ui import Button, Select, View, Modal

from bot.config import redis_config as rc 
from colorama import Fore, Back, Style

from ..handling import rRedis