import datetime
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from app.bots.database.database import dbMaria
import config 
import logging
from unicodedata import category
import asyncio

class ticket_system_report(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="new_ticket_system_report", description="Система тикетов для > Репортов")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_system_report(self, interaction: discord.Interaction):
        Embed = discord.Embed(title="📌🞄 Создайте тикет для - Репортов!", description="Нажмите на кнопку чтобы создать тикет", color=0xffffff)
        Embed.set_author(name=f"{config.ticket_system_author}")
        Embed.set_footer(text="``Статус тикетов: Работает``")

        embed_main = discord.Embed(color=0xffffff, title="🌏 ‧ 𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨", description="""
- Если вы столкнулись с какой-либо **проблемой**
на сервере, будь то **нарушение** *правил*, *баг*, 
или просто нужна *помощь*, 
``ᴄоздᴀйᴛᴇ ᴛиᴋᴇᴛ ʙ нᴀɯᴇй ᴄиᴄᴛᴇʍᴇ!``
- **__Спасибо за ваше сотрудничество!)__**
- <#1205649863937761370>

- Если вы хотите **Создать Тикет**
    - Нажмите на кнопку *__Создать Тикет__*
""")
        embed_main.set_footer(text="**𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨**  [✅]")
        embed_main.set_image(url="https://i.imgur.com/38rEjs8.png")

        view = create_ticket_reports()

        await interaction.channel.send(embed=embed_main)
        await interaction.channel.send(embed=Embed, view=view)
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_report{Fore.RESET}")
        await interaction.response.send_message("ticket_system_start_reports", ephemeral=True)


class create_ticket_reports(View):    
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Создать тикет", style=discord.ButtonStyle.green, custom_id="ticket_button_report", emoji="🎟")
    @app_commands.checks.has_permissions(send_messages=True)
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal_windows = await interaction.response.send_modal(modal_window_ticket_system_report())
        if modal_windows is None:
            print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        else:
            await modal_windows.delete()






@app_commands.describe(problem="Проблема", description_problem="Подробное описание:")
class modal_window_ticket_system_report(discord.ui.Modal, title="📌🞄 заполните пункты для: репортов"):
    problem = discord.ui.TextInput(label="Проблема", placeholder="Опишите вашу проблему в крации", style=discord.TextStyle.short)
    description_problem = discord.ui.TextInput(label="Подробное описание:", placeholder="Сформулируйте максимально вашу проблему", style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction: discord.Interaction):
        by_category = discord.utils.get(interaction.guild.categories, id=config.ticket_system_report_category)
        ticket = utils.get(interaction.guild.channels, name=f"report-{interaction.user.name}-{interaction.user.id}")
        if ticket is not None:
            await interaction.response.send_message("Ты уже создал тикет!", ephemeral=True)
            return
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True)
        }
        channel = await interaction.guild.create_text_channel(f"report-{interaction.user.name}-{interaction.user.id}", category=by_category, overwrites=overwrites, reason=f"Тикеты {interaction.user}")
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        if channel.category is not None:
            embed_ticket_player = discord.Embed(title=f"Тикет ID:``{channel.id}``", description=f"----", color= discord.Colour.blue())
            embed_ticket_player.add_field(name=f"Канал: {channel.mention}", value="")
            embed_ticket_player.add_field(name=f"Проблема", value=f"{self.problem}", inline=False)
            embed_ticket_player.add_field(name=f"Подробное описание", value=f"{self.description_problem}", inline=False)
            message_id = await channel.send(f"{interaction.user.mention}",embed=embed_ticket_player)
            embed_message_control_tickets = discord.Embed(title=f"Тикет ID:``{channel.id}``", description=f"{interaction.user.mention} создал тикет - по репортам")
            embed_message_control_tickets.add_field(name=f"Где находится : ", value=f"Канал: {channel.mention}")
            control_message = interaction.guild.get_channel(config.ticket_system_report_channel_request)
            message_id_control = await control_message.send(embed=embed_message_control_tickets, view=buttons_on_control_ticket_by_moderator())
            data = {
                "chat_id": channel.id,
                "message_id_control_panel": message_id_control.id,
                "message_id": message_id.id,
                "user_name": interaction.user.name,
                "user_id": interaction.user.id,
                "data_create_ticket": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            sync_database = await save_ticket_create(data=data,table_name="tickets")
            if sync_database is False:
                print(f"Error saving ticket to database: {sync_database}")
                return await interaction.response.send_message("Ошибка при сохранении тикета в базу данных!", ephemeral=True)
            else:
                # await interaction.user.send(embed=embed_ticket_player)
                await interaction.response.send_message("Тикет создан!", ephemeral=True)
        else:
            print(f"Error creating ticket: Category not found.")
            return await interaction.response.send_message("Ошибка при создании канала в категории!", ephemeral=True)


class buttons_on_control_ticket_by_moderator(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.plus_button_clicked_by_user = False
    @discord.ui.button(label="Информация", style=discord.ButtonStyle.gray, custom_id="ticket_button_info", emoji="🌎")
    @app_commands.checks.has_permissions(administrator=True)
    async def info_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed_information_how_to_use = discord.Embed(title="Информация", description="Кнопка для информации о тикете.", color= discord.Colour.dark_grey())
            await interaction.response.send_message(embed=embed_information_how_to_use, ephemeral=True)
        except Exception as e:
            print(f"Error touch button: {e}")
            return await interaction.response.send_message("Ошибка при нажатии на кнопку!", ephemeral=True)
    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="ticket_button_consideration", emoji="🗡")
    @app_commands.checks.has_permissions(administrator=True)
    async def consideration_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            if not self.plus_button_clicked_by_user:
                self.plus_button_clicked_by_user = True
                ticket_data = dbMaria.get_data_by_condition(condition_column='message_id_control_panel', condition_value=interaction.message.id, table_name='tickets')
                self.db_manager.update_data('tickets', new_data={
                    'user_moderator_id': interaction.user.id,
                    'user_moderator_name': interaction.user.name, 
                    'data_open_ticket': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }, condition_column='message_id_control_panel', condition_value=interaction.message.id)  
                button.disabled = True  # Устанавливаем состояние кнопки как отключенную
                await interaction.response.defer_update()  # Отложенное обновление для отображения отключенной кнопки
                if ticket_data:
                    message_id_str = ticket_data[0][1]
                    message_id_int = int(message_id_str)
                    channel_id = message_id_int
                    channel = interaction.guild.get_channel(channel_id)
                    if channel:
                        embed_control = discord.Embed(title="Тикет рассматривается", description=f"Куратор: <@{interaction.user.id}> канал: {interaction.channel.mention}", color=discord.Colour.dark_grey())
                        await channel.send(embed=embed_control, view=control_ticket_system_users()) # view=buttons_control_ticket()
                        await interaction.response.send_message(f"(id) - Тикет рассматривается {interaction.user.mention}!", ephemeral=True)
                        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}consideration ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
                    else:
                        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}channel not found: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
                else:
                    await interaction.response.send_message(f"Не удалось получить данные о тикете из базы данных!", ephemeral=True)
            else:
                await interaction.response.send_message(f"Тикет уже рассматривается!", ephemeral=True)
        except Exception as e:
            print(f"Error touch button: {e}")
            return await interaction.response.send_message("Ошибка при нажатии на кнопку!", ephemeral=True)


class control_ticket_system_users(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.db_manager = dbMaria()
    @discord.ui.button(label="Закрыть тикет!", style=discord.ButtonStyle.red, custom_id="control_system_ticket_close")
    @app_commands.checks.has_permissions(administrator=True)
    async def close_ticket_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = self.db_manager.get_data_by_condition(condition_column='chat_id', condition_value=interaction.channel.id, table_name='tickets')
        user_id_str = user[0][6]
        user_id_int = int(user_id_str)
        if user_id_int != interaction.user.id:
            await interaction.response.send_message(f"У вас нет прав закрыть этот тикет!", ephemeral=True)
        else:
            await interaction.channel.delete()
            await interaction.response.send_message(f"Тикет закрыт!", ephemeral=True)
            print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}close ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")



async def save_ticket_create(data: dict, table_name: str) -> None:
    try:
        response_database = await dbMaria.insert_data(table_name, data)
        print(f"{Fore.RED}{data['user_id']} {Fore.YELLOW}created ticket: {Fore.GREEN}{table_name}{Fore.RESET}")
        return {"success": True, "error": None}
    except Exception as e:
        print(f"Error saving ticket to database: {e}")
        return {"success": False, "error": str(e)}

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [ticket_system_report]
    for cog in cogs:
        try:
            await client.add_cog(cog(client), guilds=[discord.Object(id=1200955239281467422)])
            print(f"{Fore.GREEN}Cog '{Fore.RED}{cog}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}{cog}{Fore.GREEN}': {e}{Style.RESET_ALL}")
