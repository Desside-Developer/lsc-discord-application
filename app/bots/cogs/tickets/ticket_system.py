import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
import cogs.database.database as dbMaria
import config 
import logging
from cogs.tickets.my_commands.report_system import button_create_ticket_report, modal_window_ticket_system_report
print = logging.info

class tickets_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    # --------------------------------------------------------------------------------------------------------------------------------
    # . /ticket-system-report = Система тикетов для > Репортов
    # --------------------------------------------------------------------------------------------------------------------------------
    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        if interaction.component.custom_id == "ticket_button_report":
            await modal_window_ticket_system_report(interaction)
    @app_commands.command(name="ticket-system-report", description="Система тикетов для > Репортов")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_system_report(self, interaction: discord.Interaction):
        
        embed = discord.Embed(title="📌🞄 Создайте тикет для - Репортов!", description="Нажмите на кнопку чтобы создать тикет", color= discord.Colour.dark_red())
        embed.set_author(name=f"{config.ticket_system_author}")
        embed.set_footer(text="``Статус тикетов: Работает``")
        
        view = button_create_ticket_report()
        self.client.add_view(view)
        
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Тикет создан!", ephemeral=True)
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_report{Fore.RESET}")
    # --------------------------------------------------------------------------------------------------------------------------------
    # . /ticket-system-cheap = Система тикетов для > Установки чипа
    # --------------------------------------------------------------------------------------------------------------------------------
    # @app_commands.command(name="ticket-system-cheap", description="Система тикетов для > Установки чипа")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def ticket_system_cheap(self, interaction: discord.Interaction):
        
    #     embed = discord.Embed(title="💿🞄 Создайте тикет для - Установки чипа!", description="Нажмите на кнопку чтобы создать тикет", color= discord.Colour.dark_grey())
    #     embed.set_author(name=f"{config.ticket_system_author}")
    #     embed.set_footer(text="``Статус тикетов: Работает``")
        
    #     view = create_ticket()
        
    #     await interaction.channel.send(embed=embed, view=view)
    #     await interaction.response.send_message("Тикет создан!", ephemeral=True)
        
    #     print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_cheap{Fore.RESET}")
    # --------------------------------------------------------------------------------------------------------------------------------
    # . /ticket-system-set = Система тикетов для > Настройка Авто
    # --------------------------------------------------------------------------------------------------------------------------------
    # @app_commands.command(name="ticket-system-set", description="Система тикетов для > Настройка Авто")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def ticket_system_set(self, interaction: discord.Interaction):
    #     embed = discord.Embed(title="⏰🞄 Создайте тикет для - Настройки Авто!", description="Нажмите на кнопку чтобы создать тикет", color= discord.Colour.dark_grey())
    #     embed.set_author(name=f"{config.ticket_system_author}")
    #     embed.set_footer(text="``Статус тикетов: Работает``")

    #     view = create_ticket()

    #     await interaction.channel.send(embed=embed, view=view)
    #     await interaction.response.send_message("Тикет создан!", ephemeral=True)

    #     print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_set{Fore.RESET}")
    # --------------------------------------------------------------------------------------------------------------------------------
    # . /ticket-system-rep = Система тикетов для > Починки Двигателя
    # --------------------------------------------------------------------------------------------------------------------------------
    # @app_commands.command(name="ticket-system-rep", description="Система тикетов для > Починки Двигателя")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def ticket_system_rep(self, interaction: discord.Interaction):
    #     embed = discord.Embed(title="🔧🞄 Создайте тикет для - Починки Двигателя!", description="Нажмите на кнопку чтобы создать тикет", color= discord.Colour.dark_grey())
    #     embed.set_author(name=f"{config.ticket_system_author}")
    #     embed.set_footer(text="``Статус тикетов: Работает``")

    #     view = create_ticket()

    #     await interaction.channel.send(embed=embed, view=view)
    #     await interaction.response.send_message("Тикет создан!", ephemeral=True)

    #     print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_rep{Fore.RESET}")
    # --------------------------------------------------------------------------------------------------------------------------------
    # . /ticket-system-rent = Система тикетов для > Аренда Авто
    # --------------------------------------------------------------------------------------------------------------------------------
    # @app_commands.command(name="ticket-system-rent", description="Система тикетов для > Аренда Авто")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def ticket_system_rent(self, interaction: discord.Interaction):
    #     embed = discord.Embed(title="💼🞄 Создайте тикет для - Аренда Авто!", description="Нажмите на кнопку чтобы создать тикет", color= discord.Colour.dark_grey())
    #     embed.set_author(name=f"{config.ticket_system_author}")
    #     embed.set_footer(text="``Статус тикетов: Работает``")

    #     view = create_ticket()

    #     await interaction.channel.send(embed=embed, view=view)
    #     await interaction.response.send_message("Тикет создан!", ephemeral=True)

    #     print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_rent{Fore.RESET}")
    # --------------------------------------------------------------------------------------------------------------------------------
    # . /ticket-system-feedback = Система тикетов для > Feedbacks
    # --------------------------------------------------------------------------------------------------------------------------------
    # @app_commands.command(name="ticket-system-feedback", description="Система тикетов для > Feedbacks")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def ticket_system_feedback(self, interaction: discord.Interaction):
    #     embed = discord.Embed(title="📝🞄 Создайте тикет для - Feedbacks!", description="Нажмите на кнопку чтобы создать тикет", color= discord.Colour.dark_grey())
    #     embed.set_author(name=f"{config.ticket_system_author}")
    #     embed.set_footer(text="``Статус тикетов: Работает``")

    #     view = create_ticket()

    #     await interaction.channel.send(embed=embed, view=view)
    #     await interaction.response.send_message("Тикет создан!", ephemeral=True)

    #     print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_feedback{Fore.RESET}")
    # --------------------------------------------------------------------------------------------------------------------------------
    # . /close = Для закрытия тикета.
    # --------------------------------------------------------------------------------------------------------------------------------
    # @app_commands.command(name="close", description="delete-ticket")
    # @app_commands.checks.has_permissions(move_members=True)
    # async def ticket_delete(self, interaction: discord.Interaction,):
    #     await interaction.channel.delete()
    #     await interaction.response.send_message("Тикет удален!", ephemeral=True)
    #     print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}deleted ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
    # --------------------------------------------------------------------------------------------------------------------------------




    # @app_commands.command(name="execute-sql-mariadb", description="admin")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def command_permissions(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(f'Даем разрешение на команду')
    #     db_manager = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
    #     db_manager.execute_all_sql_files_in_subfolder('sql-data')


# class create_ticket(View):    
#     def __init__(self):
#         super().__init__(timeout=None)
#     @discord.ui.button(label="Создать тикет", style=discord.ButtonStyle.green, custom_id="ticket_button", emoji="🎟")
#     @app_commands.checks.has_permissions(send_messages=True)
#     async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
#         modal_windows = await interaction.response.send_modal(service_modal_window_tickets())
#         if modal_windows is None:
#             print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
#         else:
#             await modal_windows.delete()
#             pass
        
# @app_commands.describe(title_ticket="Название тикета", description_ticket="Описание тикета", questions_client="Вопросы клиента", questions_service="Вопросы сервиса")
# class service_modal_window_tickets(discord.ui.Modal, title="info",):
#     title_ticket = discord.ui.TextInput(label="Аренда-Авто", placeholder="My name is...", style=discord.TextStyle.short)
#     description_ticket = discord.ui.TextInput(label="починка двигателя", placeholder="My name is...", style=discord.TextStyle.paragraph)
#     questions_client = discord.ui.TextInput(label="Установка чипа", placeholder="My name is...", style=discord.TextStyle.long)
#     questions_service = discord.ui.TextInput(label="Услуги по настройке", placeholder="My name is...", style=discord.TextStyle.paragraph)
#     async def on_submit(self, interaction: discord.Interaction):
#         by_category = discord.utils.get(interaction.guild.categories, id=services_category)
#         ticket = utils.get(interaction.guild.channels, name=f"service-{interaction.user.name}-{interaction.user.id}")
#         if ticket is not None:
#             await interaction.response.send_message("Ты уже создал тикет!", ephemeral=True)
#             return
#         overwrites = {
#             interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
#             interaction.user: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True),
#             interaction.guild.me: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True)
#         }
#         channel = await interaction.guild.create_text_channel(f"service-{interaction.user.name}-{interaction.user.id}", category=by_category, overwrites=overwrites, reason=f"Тикеты {interaction.user}")
#         embed_ticket_player = discord.Embed(title=f"Тикет ID:``{interaction.user.id}``", description=f"{interaction.user.mention} Вы создали свой тикет!", color= discord.Colour.blue())
#         embed_ticket_player.add_field(name=f"Канал: {channel.mention}", value="")
#         embed_ticket_player.add_field(name="Название тикета", value=f"{self.title_ticket.value}", inline=True)
#         embed_ticket_player.add_field(name="Описание тикета", value=f"{self.description_ticket.value}", inline=False)
#         embed_ticket_player.add_field(name="Вопросы клиента", value=f"{self.questions_client.value}", inline=True)
#         embed_ticket_player.add_field(name="Вопросы сервиса", value=f"{self.questions_service.value}", inline=True)
#         message_id = await channel.send(embed=embed_ticket_player)
#         embed_message_control_tickets = discord.Embed(title=f"Тикет ID:``{interaction.user.id}``", description=f"{interaction.user.mention} создал тикет - по услугам")
#         embed_message_control_tickets.add_field(name=f"Где находится : ", value=f"Канал: {channel.mention}")
#         control_message = interaction.guild.get_channel(ticket_channel_request)
#         message_id_control_panel = await control_message.send(embed=embed_message_control_tickets,view=buttons_on_control_ticket_by_moderator())
#         await interaction.response.send_message("Тикет создан!", ephemeral=True)
#         print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}form fill: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
#         db = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
#         db.insert_data('tickets', data={'chat_id': channel.id, 'message_id_control_panel': message_id_control_panel.id, 'message_id': message_id.id, 'user_name': interaction.user.name, 'user_id': interaction.user.id})
#         pass


# class create_ticket_reports(View):    
#     def __init__(self):
#         super().__init__(timeout=None)
#     @discord.ui.button(label="Создать тикет", style=discord.ButtonStyle.green, custom_id="ticket_button_report", emoji="🎟")
#     @app_commands.checks.has_permissions(send_messages=True)
#     async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
#         modal_windows = await interaction.response.send_modal(modal_window_ticket_system_report())
#         if modal_windows is None:
#             print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
#         else:
#             await modal_windows.delete()
#             pass


# @app_commands.describe(problem="Проблема", description_problem="Подробное описание:")
# class modal_window_ticket_system_report(discord.ui.Modal, title="📌🞄 заполните пункты для: репортов"):
#     problem = discord.ui.TextInput(label="Проблема", placeholder="Опишите вашу проблему в крации", style=discord.TextStyle.short)
#     description_problem = discord.ui.TextInput(label="Подробное описание:", placeholder="Сформулируйте максимально вашу проблему", style=discord.TextStyle.paragraph)
#     async def on_submit(self, interaction: discord.Interaction):
#         by_category = discord.utils.get(interaction.guild.categories, id=config.ticket_system_report_category)
#         ticket = utils.get(interaction.guild.channels, name=f"report-{interaction.user.name}-{interaction.user.id}")
#         if ticket is not None:
#             await interaction.response.send_message("Ты уже создал тикет!", ephemeral=True)
#             return
#         overwrites = {
#             interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
#             interaction.user: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True),
#             interaction.guild.me: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True)
#         }
#         channel = await interaction.guild.create_text_channel(f"report-{interaction.user.name}-{interaction.user.id}", category=by_category, overwrites=overwrites, reason=f"Тикеты {interaction.user}")
#         embed_ticket_player = discord.Embed(title=f"Тикет ID:``{interaction.user.id}``", description=f"{interaction.user.mention} Вы создали свой тикет!", color= discord.Colour.blue())
#         embed_ticket_player.add_field(name=f"Проблема", value=f"{self.problem}", inline=True)
#         embed_ticket_player.add_field(name=f"Подробное описание", value=f"{self.description_problem}", inline=False)
#         message_id = await channel.send(embed=embed_ticket_player)
#         await interaction.response.send_message("Тикет создан!", ephemeral=True)


class buttons_on_control_ticket_by_moderator(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="+", style=discord.ButtonStyle.gray, custom_id="ticket_button_consideration")
    @app_commands.checks.has_permissions(administrator=True)
    async def consideration_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
        ticket_data = db.get_data_by_condition(condition_column='message_id_control_panel', condition_value=interaction.message.id, table_name='tickets')
        db.update_data('tickets', new_data={'user_moderator_id': interaction.user.id, 'user_moderator_name': interaction.user.name}, condition_column='message_id_control_panel', condition_value=interaction.message.id)
        if ticket_data:
            message_id_str = ticket_data[0][1]
            message_id_int = int(message_id_str)
            channel_id = message_id_int
            channel = interaction.guild.get_channel(channel_id)
            if channel:
                embed_control = discord.Embed(title="Тикет рассматривается", description=f"Куратор: <@{interaction.user.id}> канал: {interaction.channel.mention}", color= discord.Colour.dark_grey())
                await channel.send(embed=embed_control) # view=buttons_control_ticket()
                await interaction.response.send_message(f"(id) - Тикет рассматривается {interaction.user.mention}!", ephemeral=True)
            else:
                print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}channel not found: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        else:
            await interaction.response.send_message(f"Не удалось получить данные о тикете из базы данных!", ephemeral=True)


"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        cogs = [tickets_system]
        for cog in cogs:
            try:
                # client.add_view(buttons_on_control_ticket_by_moderator())
                # client.add_view(create_ticket())
                client.add_view(button_create_ticket_report())
                await client.add_cog(cog(client))
                print(f"{Fore.GREEN}Cog '{Fore.RED}{cog}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error adding cog '{Fore.RED}{cog}{Fore.GREEN}': {e}{Style.RESET_ALL}")
                continue
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}{tickets_system}{Fore.GREEN}': {e}{Style.RESET_ALL}")
