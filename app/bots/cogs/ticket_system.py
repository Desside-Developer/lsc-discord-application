import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
import cogs.database.database as dbMaria

import logging
print = logging.info

# Logs
ticket_channel_request = 1205648821871444040
channel_logs_tickets_service = 1205648797422719046
# Category
services_category = 1213181088076267661

class tickets_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="ticket-system-001", description="create-ticket-system-services")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket(self, interaction: discord.Interaction,):
        embed = discord.Embed(title="Данный тикет для сервисов", description="Нажмите на кнопку чтобы создать тикет", color= discord.Colour.blue())
        embed.set_author(name="Gustavs")
        embed.set_footer(text="@ПОчитайте правила!")
        await interaction.channel.send(embed=embed, view=create_ticket())
        await interaction.response.send_message("Тикет создан!", ephemeral=True)
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        pass
    @app_commands.command(name="close", description="delete-ticket")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_delete(self, interaction: discord.Interaction,):
        await interaction.channel.delete()
        await interaction.response.send_message("Тикет удален!", ephemeral=True)
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}deleted ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        pass
    # 
    @app_commands.command(name="execute-sql-mariadb", description="admin")
    @app_commands.checks.has_permissions(administrator=True)
    async def command_permissions(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Даем разрешение на команду')
        db_manager = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
        db_manager.execute_all_sql_files_in_subfolder('sql-data')
class create_ticket(discord.ui.View):
    def __init__(self):
        super().__init__()
        pass
    @discord.ui.button(label="Создать тикет", style=discord.ButtonStyle.green, custom_id="ticket_button")
    @app_commands.checks.has_permissions(send_messages=True)
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal_windows = await interaction.response.send_modal(service_modal_window_tickets())
        if modal_windows is None:
            print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        else:
            await modal_windows.delete()
            pass
    
class buttons_on_control_ticket_by_moderator(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.plus_button_clicked_by_user = False
    # @discord.ui.button(label="Удалить тикет", style=discord.ButtonStyle.red, custom_id="ticket_button_delete")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     ticket = utils.get(interaction.guild.channels, name=f"service-{interaction.user.name}-{interaction.user.id}")
    #     await ticket.delete()
    #     await interaction.response.send_message("Тикет удален!")
    #     print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}deleted ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
    #     pass
    # @discord.ui.button(label="Одобрить тикет", style=discord.ButtonStyle.gray, custom_id="ticket_button_accept")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def accept_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     if self.plus_button_clicked_by_user.get:
    #         db = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
    #         data_player = db.get_data_by_condition(condition_column='message_id_control_panel', condition_value=interaction.message.id, table_name='tickets')
    #         user_id_str = data_player[0][6]
    #         user_id_int = int(user_id_str)
    #         user_id = user_id_int
    #         if interaction.user.id == user_id:
    #             print('NOT NORAML')
    #         else:                
    #             interaction.response.send_message(f"(id) - Тикет одобрил {interaction.user.mention}!", ephemeral=True)
    #             embed_logs = discord.Embed(title="Тикет принят", description=f"Куратор: <@{interaction.user.id}> канал: {interaction.channel.mention}", color= discord.Colour.dark_grey())
    #             await interaction.guild.get_channel(channel_logs_tickets_service).send(embed=embed_logs)
    #     else:
    #         await interaction.response.send_message(f"Нельзя одобрить тикет, не рассмотрев его сначала!", ephemeral=True)
    @discord.ui.button(label="+", style=discord.ButtonStyle.gray, custom_id="ticket_button_consideration")
    @app_commands.checks.has_permissions(administrator=True)
    async def consideration_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.plus_button_clicked_by_user:
            self.plus_button_clicked_by_user = True
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
        else:
            await interaction.response.send_message(f"Тикет уже рассматривается!", ephemeral=True)
        # await interaction.channel_id(chat_id).send(f"(id) - Тикет рассматривается {interaction.user.mention}!")

        # clientData = discord.Embed(title="Вы приняли заявку!", description="**Можете начинать диалог с клиентом**", color=discord.Colour.dark_grey())
        # embed = discord.Embed(title="Статус выставлен у тикета ``на рассмотрении``", description=f"Куратор: <@{interaction.user.id}>", color=discord.Colour.dark_grey())
        # embed.set_author(name="Gustavs")

        # await interaction.response.send_message(embed=embed)
        # await interaction.response.send_message(embed=clientData, ephemeral=True)


@app_commands.describe(title_ticket="Название тикета", description_ticket="Описание тикета", questions_client="Вопросы клиента", questions_service="Вопросы сервиса")
class service_modal_window_tickets(discord.ui.Modal, title="info",):
    title_ticket = discord.ui.TextInput(label="Название тикета", placeholder="My name is...", style=discord.TextStyle.short)
    description_ticket = discord.ui.TextInput(label="Описание тикета", placeholder="My name is...", style=discord.TextStyle.short)
    questions_client = discord.ui.TextInput(label="Вопросы клиента", placeholder="My name is...", style=discord.TextStyle.short)
    questions_service = discord.ui.TextInput(label="Вопросы сервиса", placeholder="My name is...", style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        by_category = discord.utils.get(interaction.guild.categories, id=services_category)
        ticket = utils.get(interaction.guild.channels, name=f"service-{interaction.user.name}-{interaction.user.id}")
        if ticket is not None:
            await interaction.response.send_message("Ты уже создал тикет!", ephemeral=True)
            return
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True)
        }
        channel = await interaction.guild.create_text_channel(f"service-{interaction.user.name}-{interaction.user.id}", category=by_category, overwrites=overwrites, reason=f"Тикеты {interaction.user}")
        embed_ticket_player = discord.Embed(title=f"Тикет ID:``{interaction.user.id}``", description=f"{interaction.user.mention} Вы создали свой тикет!", color= discord.Colour.blue())
        embed_ticket_player.add_field(name=f"Канал: {channel.mention}", value="")
        embed_ticket_player.add_field(name="Название тикета", value=f"{self.title_ticket.value}", inline=True)
        embed_ticket_player.add_field(name="Описание тикета", value=f"{self.description_ticket.value}", inline=False)
        embed_ticket_player.add_field(name="Вопросы клиента", value=f"{self.questions_client.value}", inline=True)
        embed_ticket_player.add_field(name="Вопросы сервиса", value=f"{self.questions_service.value}", inline=True)
        message_id = await channel.send(embed=embed_ticket_player)
        embed_message_control_tickets = discord.Embed(title=f"Тикет ID:``{interaction.user.id}``", description=f"{interaction.user.mention} создал тикет - по услугам")
        embed_message_control_tickets.add_field(name=f"Где находится : ", value=f"Канал: {channel.mention}")
        control_message = interaction.guild.get_channel(ticket_channel_request)
        message_id_control_panel = await control_message.send(embed=embed_message_control_tickets,view=buttons_on_control_ticket_by_moderator())
        await interaction.response.send_message("Тикет создан!", ephemeral=True)
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}form fill: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        db = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
        db.insert_data('tickets', data={'chat_id': channel.id, 'message_id_control_panel': message_id_control_panel.id, 'message_id': message_id.id, 'user_name': interaction.user.name, 'user_id': interaction.user.id})
        pass


# class buttons_control_ticket(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#     @discord.ui.button(label="Открыть", style=discord.ButtonStyle.green, custom_id="ticket_button_open")
#     async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
#         db = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
#         data = db.get_data_by_condition(condition_column='user_moderator_id', condition_value=interaction.user.id, table_name='tickets')
#         user_moderator_id = data[0][6]
#         user_moderator_id = int(user_moderator_id)
#         if user_moderator_id == 0:
#             await interaction.response.send_message(f"Ты не можешь открыть тикет!", ephemeral=True)
#             return
#         else:
#             user_id = data[0][5] ; chat_id = data[0][1]
#             if not isinstance(user_id, int):
#                 raise ValueError("user_id должен быть целым числом")
#             if not isinstance(chat_id, int):
#                 raise ValueError("chat_id должен быть целым числом")
#             channel = discord.utils.get(interaction.guild.channels, id=chat_id)
#             await channel.set_permissions(user_id, read_messages=True, view_channel=True, send_messages=True, embed_links=True, read_message_history=True)
#             embed_open_ticket = discord.Embed(title=f"Тикет ID:``{user_id}``", description=f"Для <@{user_id}> открыл тикет!", color=discord.Colour.blue())
#             await interaction.response.send_message(embed=embed_open_ticket)
    

"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(tickets_system(client))
        print(f"{Fore.GREEN}Cog '{Fore.RED}{tickets_system}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}{tickets_system}{Fore.GREEN}': {e}{Style.RESET_ALL}")
