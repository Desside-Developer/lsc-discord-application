import discord
import json
import os
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from app.bots.database.database import dbMaria
import config 
import logging
import requests
import asyncio

print = logging.info

class embed_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        # Запускаем обновление статуса сервера
        self.message = None
        self.client.loop.create_task(self.update_server_status())
    async def update_server_status(self):
        await self.client.wait_until_ready()
        channel_id = '1214790923133779971'

        while not self.client.is_closed():
            try:
                # Получаем информацию о сервере GTA 5 RP
                response = requests.get(f"https://cdn.rage.mp/master/")
                if response.status_code == 200:
                    data = response.json()
                    server_info = data.get("s1.arizona-v.com:22005", {})  # Получаем информацию о сервере

                    players_count = server_info.get("players", None)
                    max_players_count = server_info.get("maxplayers", None)
                    host_url = server_info.get("url", None)

                    # if players_count is not None:
                        # print(f"Количество игроков на сервере: {players_count}")
                    # else:
                        # print("Информация о количестве игроков недоступна.")
                else:
                    print(f"Ошибка при запросе: {response.status_code}")
                    
                    
                # Обновляем embed с информацией о сервере
                embed = discord.Embed(title="👋🞄 Arizona Liberty!", description="---", color=discord.Colour.light_grey())
                embed.set_image(url="https://i.imgur.com/DG9y5ZS.png")
                embed.add_field(name="Игроков онлайн:", value=f"{players_count}", inline=True)
                embed.add_field(name="Оффициальная ссылка:", value=f"{host_url}", inline=True)
                embed.add_field(name="Макс игроков:", value=f"{max_players_count}", inline=False)
                embed.set_author(name="📌🞄 Status Servers")
                embed.set_footer(text="---")

                # Если сообщение еще не отправлено, отправляем его
                if not self.message:
                    channel = self.client.get_channel(int(channel_id))
                    self.message = await channel.send(embed=embed)
                else:
                    # Если сообщение уже отправлено, редактируем его содержимое
                    await self.message.edit(embed=embed)

            except Exception as e:
                print(f"Ошибка при обновлении статуса сервера: {e}")

            # Ждем 10 секунд перед следующим обновлением
            await asyncio.sleep(10)



"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [embed_system]
    for cog in cogs:
        try:
            await client.add_cog(cog(client))
            print(f"{Fore.GREEN}Cog '{Fore.RED}{cog}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}{cog}{Fore.GREEN}': {e}{Style.RESET_ALL}")
            continue
