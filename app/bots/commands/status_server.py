import discord
import json
import os
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria
import config 
import logging
import requests
import asyncio

print = logging.info

class embed_system_status(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.message_id = '1222366421107998801'  # Установите здесь ваш ID сообщения
        self.client.loop.create_task(self.update_server_status())
    @commands.command(name="embed_update_status")
    @commands.is_owner()
    async def update_status_embed(self, ctx):
        await ctx.message.delete()
        Embed = discord.Embed(title="👋🞄 Arizona Liberty!", description="""""", color=0xffffff)
        Embed.add_field(name="Игроков онлайн:", value=f"0", inline=True)
        Embed.add_field(name="Оффициальная ссылка:", value=f"no url", inline=True)
        Embed.add_field(name="Макс игроков:", value=f"0", inline=False)
        Embed.set_author(name="📌🞄 Status Servers")
        Embed.set_image(url="https://i.imgur.com/AVANWHG.png")
        await ctx.send(embed=Embed)

    async def update_server_status(self):
        await self.client.wait_until_ready()
        channel_id = '1214790923133779971'
        while not self.client.is_closed():
            try:
                response = requests.get(f"https://cdn.rage.mp/master/")
                if response.status_code == 200:
                    data = response.json()
                    server_info = data.get("s1.arizona-v.com:22005", {})

                    players_count = server_info.get("players", None)
                    max_players_count = server_info.get("maxplayers", None)
                    host_url = server_info.get("url", None)

                    embed = discord.Embed(title="👋🞄 Arizona Liberty!", description="", color=0xffffff)
                    embed.add_field(name="🎙 ⭑ Игроков онлайн:", value=f"{players_count}", inline=True)
                    embed.add_field(name="🎙 ⭑ Оффициальная ссылка:", value=f"{host_url}", inline=True)
                    embed.add_field(name="🎙 ⭑ Макс игроков:", value=f"{max_players_count}", inline=False)
                    embed.set_author(name="📌🞄 Status Servers")
                    embed.set_image(url="https://i.imgur.com/AVANWHG.png")

                    channel = self.client.get_channel(int(channel_id))
                    message = await channel.fetch_message(self.message_id)
                    await message.edit(embed=embed)

            except Exception as e:
                print(f"Ошибка при обновлении статуса сервера: {e}")

            await asyncio.sleep(10)



"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [embed_system_status]
    for cog in cogs:
        try:
            await client.add_cog(cog(client))
            print(f"{Fore.GREEN}Cog '{Fore.RED}embed_system_status{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}embed_system_status{Fore.GREEN}': {e}{Style.RESET_ALL}")
            continue
