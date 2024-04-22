import discord
from discord import app_commands, utils, HTTPException
from discord.ext import commands as cm
from discord.ui import Button, Select, View, Modal

# from .routes import *
from .handlers import interactions
from colorama import Fore, Back, Style
import logging

# from .settings import *

import redis

class CustomLogging():
    logger: logging
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
    def log(self, message):
        self.logger.info(message)
print = CustomLogging().log 