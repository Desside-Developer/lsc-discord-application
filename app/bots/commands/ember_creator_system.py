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
    @app_commands.command(name="hello-world", description="hello")
    async def hello_world(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello World!")
    @app_commands.command(name="embed-ticket-system-cheap", description="Вывод красивых сообщений для > Установка Чипа")
    @app_commands.checks.has_permissions(administrator=True)
    async def embed_ticket_system_cheap(self, interaction: discord.Interaction):
        embed_main = discord.Embed(title="LSC - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚ς: 🞄 Установка Чип-Тюнинга", color=discord.Colour.green())
        embed_main.set_author(name="**Увеличьте мощность вашего авто!**", icon_url="https://i.imgur.com/8txHSse.png")
        embed_main.description = """
        **Хотите улучшить характеристики вашего автомобиля?**

        **LSC - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚ς** предлагает установку чип-тюнинга!

        **Что такое чип-тюнинг?**

        Чип-тюнинг - это изменение программного обеспечения 
        блока управления двигателем (ЭБУ) 
        для увеличения мощности и крутящего момента.

        **Преимущества чип-тюнинга:**

        * **Повышение мощности:** 
            * Увеличьте мощность вашего 
            * автомобиля на 10-20%.
        * **Улучшение динамики:** 
            * Ваш автомобиль станет 
            * более динамичным и отзывчивым.
        * **Снижение расхода топлива:** 
            * Чип-тюнинг может 
            * привести к экономии топлива.

        **Наши предложения:**

        * **49% шанс:** 100.000$
        * **59% шанс:** 300.000$
        * **69% шанс:** 1.000.000$
        * **79% шанс:** 2.500.000$

        **Как начать:**

        1. **Нажмите кнопку "Создать тикет".**
        2. **Выберите желаемый шанс.**
        3. **Оплатите услугу.**
        4. **Привезите ваш автомобиль в наш сервис.**

        **Наши специалисты** установят чип-тюнинг 
        в кратчайшие сроки.

        **---**

        **Создать тикет:**

        **URL: [https://www.canva.com/create/tickets/](https://www.canva.com/create/tickets/)**

        **---**

        **LSC - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚ς:** 
        **Ваш путь к идеальному автомобилю!**

        **---**
        """
        embed_main.set_thumbnail(url="https://i.imgur.com/8txHSse.png")
        embed_main.add_field(name="️ Как мы можем вам помочь:", value="""
        * **Увеличить мощность:** 
            * Добавьте 10-20% к мощности 
            * вашего автомобиля.
        * **Улучшить динамику:** 
            * Сделайте ваш автомобиль 
            * более динамичным и отзывчивым.
        * **Снизить расход топлива:** 
            * Экономьте на бензине 
            * с помощью чип-тюнинга.

        **---**

        **LSC - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚ς:** 
        **Больше мощности - больше драйва!**
        """, inline=False)
        embed_main.set_footer(text="LSC - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚ς")
        await interaction.response.send_message(embed=embed_main)
        await interaction.response.send_message("Ready", ephemeral=True)
    @app_commands.command(name="embed-garage", description="Вывод красивых сообщений для > Наши Гаражи")
    @app_commands.checks.has_permissions(administrator=True)
    async def embed_garage(self, interaction: discord.Interaction):
        embed_main = discord.Embed(color=0xffffff, title="📌‧ нᴀɯи ᴦᴀᴩᴀжи!", description=f"""Если у вас возникают вопросы.
- Обратитесь к модераторам
- или к администраторам. ↙
- <#1205649863937761370>
        """
        )
        embed_main.set_image(url="https://i.imgur.com/sOyS2oX.png")
        embed_main.set_footer(text="**𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨**  [✅]")
    
        await interaction.channel.send(embed=embed_main)
        await interaction.response.send_message("Ready", ephemeral=True)

    @app_commands.command(name="embed-ticket-system-rep", description="Вывод красивых сообщений для > Починка двигателя")
    @app_commands.checks.has_permissions(administrator=True)
    async def embed_ticket_system_rep(self, interaction: discord.Interaction):
        embed_main = discord.Embed(color=0xffffff, title="🌏 ‧ 𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨", description="""
- Если вы столкнулись с какой-либо **проблемой**
на сервере, будь то **нарушение** *правил*, *баг*, 
или просто нужна *помощь*, 
``ᴄоздᴀйᴛᴇ ᴛиᴋᴇᴛ ʙ нᴀɯᴇй ᴄиᴄᴛᴇʍᴇ ᴩᴇᴨоᴩᴛоʙ!``
- **__Спасибо за ваше сотрудничество!)__**
- <#1205649863937761370>

- Если вы хотите **Создать Тикет**
 - Нажмите на кнопку *__Создать Тикет__*
                               """)
        embed_main.set_image(url="https://i.imgur.com/38rEjs8.png")
        await interaction.channel.send(embed=embed_main)
        await interaction.response.send_message("Ready", ephemeral=True)

    @app_commands.command(name="embed-ticket-system-set", description="Вывод красивых сообщений для > Настройка Авто")
    @app_commands.checks.has_permissions(administrator=True)
    async def embed_ticket_system_set(self, interaction: discord.Interaction):
        embed_main = discord.Embed(title="Los Santos Customs №3", color=discord.Colour.purple())
        embed_main.set_author(name="**Ваша машина - Ваш стиль!**", icon_url="https://i.imgur.com/8txHSse.png")
        embed_main.description = """
        **Los Santos Customs №3** - это тюнинг-ателье, где ваши мечты о 

        **идеальном автомобиле** станут реальностью!

        **Наши преимущества:**

        * **Минимальная наценка:** 
            * Мы предлагаем самые выгодные цены 
            * на тюнинг в Los Santos.
        * **Все настройки по 250.000$:** 
            * Доступны любые изменения 
            * для вашего автомобиля.
        * **Услуга настройщика:** 
            * Наши опытные мастера 
            * помогут вам создать неповторимый стиль.

        **Как начать:**

        1. **Приезжайте в Los Santos Customs №3.**
        2. **Выберите желаемые настройки.**
        3. **Оплатите услугу.**
        4. **Наслаждайтесь своим обновленным автомобилем!**

        **---**

        **Услуга настройщика:** 1.000.000$

        **Оплата:** Сначала оплата, а потом услуги!

        **---**

        **Los Santos Customs №3:** 
        **Ваш путь к идеальному автомобилю!**

        **---**
        """
        embed_main.set_thumbnail(url="https://i.imgur.com/8txHSse.png")
        embed_main.add_field(name="️ Что мы можем вам предложить:", value="""
        * **Тюнинг:** 
            * Широкий выбор колесных дисков, 
            * спойлеров, бамперов, 
            * выхлопных систем и многое другое.
        * **Персонализация:** 
            * Изменение цвета, 
            * установка неоновой подсветки, 
            * виниловых наклеек и других элементов.
        * **Улучшение характеристик:** 
            * Чип-тюнинг, 
            * замена двигателя, 
            * установка турбонаддува и т.д.

        **---**

        **Los Santos Customs №3:** 
        **Сделайте ваш автомобиль уникальным!**
        """, inline=False)
        embed_main.set_footer(text="Los Santos Customs №3")
        await interaction.response.send_message(embed=embed_main)
        await interaction.response.send_message("Ready", ephemeral=True)


    @app_commands.command(name="embed-ticket-system-rent", description="Вывод красивых сообщений для > Аренда Авто")
    @app_commands.checks.has_permissions(administrator=True)
    async def embed_ticket_system_rent(self, interaction: discord.Interaction):
        embed_main = discord.Embed(color=0xe6ca00, title="💼 ‧ 𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚", description="""
``ᴄоздᴀйᴛᴇ ᴛиᴋᴇᴛ ʙ нᴀɯᴇй ᴄиᴄᴛᴇʍᴇ ᴩᴇᴨоᴩᴛоʙ!``
- **__Спасибо за ваше сотрудничество!)__**
- <#1205649863937761370>
                            """)
        embed_main.add_field(name="🟢‧ Выберите категорию", value="""
- 🛻⇢ **Легковые** автомобили
- 🚛⇢ **Грузовые** автомобили
- 🛵⇢ **Мотоциклы**
- 🛬⇢ **Самолеты**
- 🚤⇢ **Корабли**(Лодки)
                        """, inline=True)
        embed_main.add_field(name="⏱️‧ Срок", value="""
- *от 1 часа до 7 дней* (**__Спрашивайте отдельно__**)
                        """, inline=False)
        embed_main.set_footer(text="**𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨**  [✅]")
        embed_main.set_image(url="https://i.imgur.com/QMs5e9Q.png")
        await interaction.channel.send(embed=embed_main)
        await interaction.response.send_message("Ready", ephemeral=True)

    @app_commands.command(name="embed-ticket-system-report", description="Вывод красивых сообщений для > Report")
    @app_commands.checks.has_permissions(administrator=True)
    async def embed_ticket_system_report(self, interaction: discord.Interaction):
        embed_main = discord.Embed(title="LSC - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨: 🞄 Система Репортов", color=discord.Colour.dark_red())
        embed_main.set_author(name="⚠️ Важное сообщение!", icon_url="https://cdn.discordapp.com/attachments/876543210987654321/987654321098765432/warning.png")
        embed_main.description = """
        Если вы столкнулись с какой-либо проблемой на сервере, будь то нарушение правил, баг, или просто нужна помощь, создайте тикет в нашей системе репортов!

        **Как это сделать:**

        1. Нажмите кнопку **"Создать тикет"** ниже.
        2. Выберите **категорию** вашего репорта из выпадающего списка.
        3. **Опишите** вашу проблему **как можно подробнее**.
        4. **Приложите скриншоты или видео**, если это возможно.
        5. Нажмите **"Отправить"**.

        **Наши модераторы** будут уведомлены о вашем тикете и **примут меры** в кратчайшие сроки.

        **Статус системы тикетов:** 🟢 Работает

        **Создать тикет:**

        https://www.canva.com/create/tickets/

        **---**

        **Дополнительная информация:**

        * Вы можете **отслеживать статус** своих тикетов в **личном кабинете**.
        * Вы можете **ответить** на сообщения модераторов **в тикете**.
        * **Не злоупотребляйте** системой репортов.

        **---**

        **Спасибо за ваше сотрудничество!**

        **LSC - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨**

        **---**
        """
        embed_main.set_footer(text="LSC - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨")
        await interaction.response.send_message(embed=embed_main)
        await interaction.response.send_message("Ready", ephemeral=True)
    # @app_commands.command(name="embed-status-servers", description="Вывод красивых сообщений для > Онлайна и прочего серверов")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def embed_status_servers(self, interaction: discord.Interaction):
    #     embed_main = discord.Embed(title="👋🞄 Arizona Liberty!", description="---", color=discord.Colour.dark_red())
    #     embed_main.add_field(name="Игроков онлайн:", value="{players_counts}", inline=False)
    #     embed_main.set_author(name="📌🞄 Status Servers")
    #     embed_main.set_footer(text="---")
    #     await interaction.response.send_message("Ready", ephemeral=True)
    #     await interaction.channel.send(embed=embed_main)
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
