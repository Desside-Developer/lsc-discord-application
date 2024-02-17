#!/usr/bin/env python3

from discord.ext import commands
import discord
from config import Bot_music, music_cogs


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents, **kwargs)

    async def setup_hook(self):
        for cog in music_cogs:
            try:
                await self.load_extension(cog)
            except Exception as exc:
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')


intents = discord.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)


# write general commands here
# @bot.tree.command(name="create-embed", description="embed..")
# async def create_embed(interaction: discord.Interaction):
    # view = EmbedCreator(bot=bot)
    # await interaction.response.send_message(embed=view.get_default_embed, view=view)


bot.run(Bot_music)
