import os

import discord
from dotenv import load_dotenv
load_dotenv()
BOT_MODERATOR = os.getenv('BOT_MODERATOR')


class Bot1Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True

client = Bot1Client(intents=intents)
client.run(BOT_MODERATOR)
