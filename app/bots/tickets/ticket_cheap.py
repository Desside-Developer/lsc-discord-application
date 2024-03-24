import datetime
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
import config 
import logging
from unicodedata import category
import asyncio

class ticket_system_cheap(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="new_ticket_system", description="TEST", nsfw=False)
    async def ticket_system_start(self, int: discord.Interaction):
        Embed = discord.Embed(title="💿🞄 Создайте тикет для - Установки чипа!", description="Нажмите на кнопку чтобы создать тикет", color=0x942aff)
        Embed.set_author(name=f"{config.ticket_system_author}")
        Embed.set_footer(text="``Статус тикетов: Работает``")

        view = create_ticket_cheap()

        embed_cheap = discord.Embed(color=0x942aff, title="💿 ‧ 𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨", description="""
    ``ᴄоздᴀйᴛᴇ ᴛиᴋᴇᴛ ʙ нᴀɯᴇй ᴄиᴄᴛᴇʍᴇ!``
    - **__Спасибо за ваше сотрудничество!)__**
    - <#1205650012038504498>
        """)
        embed_cheap.add_field(name="❓‧ Что такое чип-тюнинг?", value="""
    Чип-тюнинг - это изменение программного обеспечения
    блока управления двигателем (__ЭБУ__)
    для увеличения мощности и крутящего момента.
        """, inline=False)
        embed_cheap.add_field(name="☑️‧ Преимущества чип-тюнинга:", value="""
    **__Повышение мощности__:**
    *Увеличьте мощность вашего автомобиля* на __10-20%__.
    **__Улучшение динамики__**: 
    *Ваш автомобиль станет* более динамичным и отзывчивым.
    **__Снижение расхода топлива__**: 
    *Чип-тюнинг может* привести к экономии топлива.
        """, inline=False)
        embed_cheap.add_field(name="🔲‧ Наши предложения", value="""
    **__49% шанс: 100.000$__**
    **__59% шанс: 300.000$__**
    **__69% шанс: 1.000.000$__**
    **__79% шанс: 2.500.000$__**
        """, inline=False)
        embed_cheap.set_image(url="https://i.imgur.com/FykvGX4.png")

        await int.channel.send(embed=embed_cheap)
        await int.channel.send(embed=Embed, view=view)
        print(f"{Fore.RED}{int.user} {Fore.YELLOW}ticket system start: {Fore.GREEN}ticket_system_cheap{Fore.RESET}")
        await int.response.send_message("Ticket_Cheap_System_Start", ephemeral=True)




class create_ticket_cheap(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Создать тикет", style=discord.ButtonStyle.green, custom_id="ticket_button_cheap", emoji="🎟")
    @app_commands.checks.has_permissions(send_messages=True)
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal_windows = await interaction.response.send_modal(modal_window_ticket_system_cheap())
        if modal_windows is None:
            print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket: {Fore.GREEN}Ticket-System-Cheap{Fore.RESET}")
        else:
            await modal_windows.delete()
            pass


@app_commands.describe(select_cheap="Установка какого уровня?", change_on_select="Выберите шанс на установку чипа")
class modal_window_ticket_system_cheap(discord.ui.Modal, title="💿🞄 заполните пункты для: установки чипа"):
    select_cheap = discord.ui.TextInput(label="Установка какого уровня?", placeholder="Например: 1,2,3,4,5", style=discord.TextStyle.short)
    change_on_select = discord.ui.TextInput(label="Выберите шанс на установку чипа", placeholder="Например: 10%", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        by_category = discord.utils.get(interaction.guild.categories, id=config.ticket_system_cheap_category)
        ticket = utils.get(interaction.guild.channels, name=f"cheap-{interaction.user.name}-{interaction.user.id}")
        if ticket is not None:
            await interaction.response.send_message("Ты уже создал тикет!", ephemeral=True)
            return
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True)
        }
        channel = await interaction.guild.create_text_channel(f"cheap-{interaction.user.name}-{interaction.user.id}", category=by_category, overwrites=overwrites, reason=f"Тикеты {interaction.user}")
        embed_ticket_player = discord.Embed(title=f"Тикет ID:``{channel.id}``", description=f"{interaction.user.mention} Вы создали свой тикет!", color= discord.Colour.blue())
        embed_ticket_player.add_field(name=f"Уровень", value=f"{self.select_cheap}", inline=True)
        embed_ticket_player.add_field(name=f"Шанс на установку", value=f"{self.change_on_select}", inline=False)
        message_id = await channel.send(embed=embed_ticket_player)
        await interaction.response.send_message("Тикет создан!", ephemeral=True, embed=embed_ticket_player)
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket: {Fore.GREEN}Ticket-System-Cheap{Fore.RESET}")


"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [ticket_system_cheap]
    for cog in cogs:
        try:
            await client.add_cog(cog(client), guilds=[discord.Object(id=1200955239281467422)])
            print(f"{Fore.GREEN}Cog '{Fore.RED} ticket_system_cheap {Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED} ticket_system_cheap {Fore.GREEN}': {e}{Style.RESET_ALL}")
