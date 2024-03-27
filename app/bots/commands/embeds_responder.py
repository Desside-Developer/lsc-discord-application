import datetime
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria
import config 
import logging
from unicodedata import category
import asyncio
print = logging.info

class embeds_responder(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @commands.command(name="embed-rules")
    @commands.is_owner()
    async def embed_rules(self, ctx: commands.Context):
        await ctx.message.delete()
        Embed = discord.Embed(title="📌🞄 Ознакомьтесь с Правилами!", description="""
``1.`` **Незнание правил сервера не освобождает от ответственности!**
(Администрация имеет полное право выдать наказание без объяснения причины)
``2.`` **На сервере пресекаются любые конфликты**!!! 
    **Запрещено**:
``2.1.`` Оскорблять **Администрацию** сервера.
``2.2.`` **Завуалированные** оскорбления
``2.3.`` Оскорбления жителей **стран,народов.**
``2.4.`` **Злоупотребление** нецензурными выражениями
``2.5``  Оскорблять
``2.6.`` Делать ники, такие же или похожие на ники Главных лиц канала или **Администрации**
``2.7.`` Любое неадекватное поведение, нарушающее спокойную и дружную атмосферу сервера     
``2.8.`` Обсуждение действий **Администрации** 
``2.9.`` **Контент 18+**
``2.10.`` Любые ссылки на каналы YOUTUBE или TWITCH, рекламы, огласки ради
``3.`` Запрещен любой вид угроз.
``4.`` Запрещен Caps-Lock, или проще, сообщения, в которых все буквы заглавные. **(К примеру: МАША ПРЕВЕД КАК ДЫЛА?)**
``5.`` Запрещены любые отрицательные разговоры про политику, если Вы не интересуетесь или не знаете, то лучше просто помолчите.
``6.`` ЗАПРЕЩЕНО упоминать Создателя и Администрацию сервера просто так, без причины. Это карается 2-мя варнами и мутом (на неопределённый срок) без предупреждения!! (Исключения только при разрешении администрации.) 
``7.`` Сервер не несет ответственности за нечестные торговли с участниками!
(**Правила будут дополняться**, если вы намеренно сделаете противозаконные действия, то администрация может запретить **Вас** или забанить **Вас** из сервера)
""", color=0x000001)
        Embed.set_image(url="https://i.imgur.com/0wbEWph.png")
        Embed.set_footer(text="𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨  [✅]")
        await ctx.send(embed=Embed)
    @commands.command(name="embed-sort")
    @commands.is_owner()
    async def embed_sort(self, ctx: commands.Context):
        await ctx.message.delete()
        Embed = discord.Embed(title="**Наш Ассортимент!**", color=0xffffff, description="""
🚚**_Коммерческий транспорт_**🚚 

Для выполнения задания **Дальнобоя**(Все **грузовики** на **4.4.4.4 + настры**):

Speedo Заказной(1т) Час 25.000$ 
• **Speedo Express**(1т) Час ``50.000$``
• **Maibatsu Mule Neo**(3т) Час ``55.000$``
• **Vapid Yankee** '90(5тонн) Час ``60.000$``

Vapid Yankee (8т) Час 80.000$ 
• **Pounder (10т)** Час ``100.000$`` 
• **MTL Brickade (10т)** Час ``100.000$`` 
• **Phantom (20тонн)** в Хром цвете +прицеп Час ``150.000$``

**Tesla Semi** (20тонн) в хроме Час ``200.000$``

🏍️**_Мотоцикл_**🏍️
**BMW S1000rr Час 60.000$**ФТ на 4-м чипе 540 на заднем колесе. Отличные настры для ловли

🏎️**_Автомобили разных классов_**🏎️ 
Все машины ФТ на 540 + настры
McLaren F1 (Limited) -4часа 750.000$ / 12-часов 1.500.000$ / 24-часа 2.500.000$

• **Toyota Supra(Дрифт-кар)** -Час ``100.000$``
• **Bugatti Wistral** -Час ``100.000$`` 
• **Ford GT** -Час ``100.000$``
• **Lamborghini Countach** -``100.000$``

• **Lamborghini Avendore SVJ**-``100.000$``
• **Maserati GranTurismo Winter** 2023-``100.000$``

• **Nissan GTR** - ``50.000$`` 
• **Mercedes-Benz GTs** - Час ``50.000$`` 
• **Issi(кошмар)**- Час ``50.000$``
• **BMW 750** - Час ``50.000$``
• **Land Cruiser 200** -Час ``50.000$``

• **Mercedes Benz** 190e -Час ``50.000$``
• **Rolls-Royse** Cullinan -Час ``50.000$`` 
• **Archel Hella** -Час ``50.000$``
• **$Ford Mustang** 1967 -Час ``50.000$``

• **Porshe 919 Turbo S** Кабриолет -Час ``50.000$`` 
• **Mercedes Benz GT63** -Час ``50.000$ ``
• **Mercedes Benz e63** -Час 50.000$Audi PS7 -Час ``50.000$`` 
• **Audi PS7** -Час ``50.000$`` • Roadster Тесла -Час ``50.000$``

🚤**_Лодки_**🚤
**𝙿𝚎𝚐𝚊𝚜𝚜𝚒 𝚃𝚎𝚌𝚗𝚘𝚠𝚊𝚛 𝚆𝚒𝚗𝚝𝚎𝚛 𝟸𝟶𝟸𝟹** 10-Часов 500к****24-часа 1кк

""")
        Embed.set_footer(text="𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨  [✅]")
        await ctx.send(embed=Embed)
    @commands.command(name="embed-info-mod")
    @commands.is_owner()
    async def embed_info_mod(self, ctx: commands.Context):
        await ctx.message.delete()
        Embed = discord.Embed(title="**Для Менеджеров**", color=0xffffff, description="""
``Названия Тикет Систем!``

💼 - ``RENT`` >

Тикет Система **Аренда Авто**
<#1214790331019567125>

🌏 - ``Report`` >

Тикет Система **Репортов на игроков**
<#1214789959739904000>

🔧 - ``Rep`` >

Тикет Система **Починки Двигателя**
<#1214790430265180222>

⏰ - ``SET`` >

Тикет Система **Настройки Авто**
<#1214790175520202773>

💿 - ``CHEAP`` >

Тикет Система **Установки Чипа**
<#1214790096155582556>

""")
        Embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        Embed.set_footer(text="𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨  [✅]")
        await ctx.send(embed=Embed)



"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(embeds_responder(client), guilds=[discord.Object(id=1200955239281467422)])
        print(f"{Fore.GREEN}Cog '{Fore.RED}embeds_responder{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}embeds_responder{Fore.GREEN}': {e}{Style.RESET_ALL}")
