import datetime
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria
from handlers.hand_package import save_ticket_for_table, generate_ticket_token, check_user
import config
import logging
print = logging.info

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
        await check_user(id=interaction.user.id, user_name=interaction.user.name)
        modal_windows = await interaction.response.send_modal(modal_window_ticket_system_report())
        if modal_windows is None:
            print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}open modal ticket: {Fore.GREEN}Репорты{Fore.RESET}")
        else:
            await modal_windows.delete()






@app_commands.describe(problem="Проблема", description_problem="Подробное описание:")
class modal_window_ticket_system_report(discord.ui.Modal, title="📌🞄 заполните пункты"):
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
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket channel: {Fore.GREEN} {channel.name} {Fore.RESET}")
        if channel.category is not None:
            token_ticket = generate_ticket_token()
            embed_ticket_player = discord.Embed(title=f"🎓 ⭑ Тикет ID:``{token_ticket}``", description=f"", color= discord.Colour.blue())
            embed_ticket_player.add_field(name=f"📃 ⭑ Канал: {channel.mention}", value="")
            embed_ticket_player.add_field(name=f"📒 ⭑ Проблема", value=f"{self.problem}", inline=False)
            embed_ticket_player.add_field(name=f"📊 ⭑ Подробное описание", value=f"{self.description_problem}", inline=False)
            await channel.send(f"{interaction.user.mention}",embed=embed_ticket_player)
            embed_message_control_tickets = discord.Embed(title=f"🎓 ⭑ Тикет ID:``{token_ticket}``", description=f"{interaction.user.mention} создал тикет - по репортам 📢")
            embed_message_control_tickets.add_field(name=f"🔑 ⭑ Где находится : ", value=f"""
📋 ⭑ Канал: {channel.mention}
📞 ⭑ Имя Пользователя: **{interaction.user.name}**
🎙 ⭑ Айди Пользователя: ``{interaction.user.id}``
🔔 ⭑ Упоминалка Данного пользователя: {interaction.user.mention}
""")
            control_message = interaction.guild.get_channel(config.ticket_system_report_channel_request)
            message_id_control = await control_message.send(embed=embed_message_control_tickets, view=buttons_on_control_ticket_by_moderator())
            sync_database = await save_ticket_for_table(ticket_id=token_ticket, user_id=interaction.user.id, status="New", channel_id=channel.id, message_id=message_id_control.id, created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if sync_database is False:
                print(f"Error saving ticket to database: {sync_database}")
                return await interaction.response.send_message("Ошибка сервера!", ephemeral=True)
            else:
                # await interaction.user.send(embed=embed_ticket_player)
                await interaction.response.send_message("Тикет создан!", ephemeral=True)
        else:
            print(f"Error creating ticket: Category not found.")
            return await interaction.response.send_message("Ошибка при создании канала в категории!", ephemeral=True)


class buttons_on_control_ticket_by_moderator(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Жалоба", style=discord.ButtonStyle.gray, custom_id="ticket_button_info", emoji="📌")
    @app_commands.checks.has_permissions(administrator=True)
    async def info_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed_information_how_to_use = discord.Embed(title="Информация", description="Кнопка для информации о тикете.", color= discord.Colour.dark_grey())
            await interaction.response.send_message(embed=embed_information_how_to_use, ephemeral=True)
        except Exception as e:
            print(f"Error touch button: {e}")
            return await interaction.response.send_message("Ошибка при нажатии на кнопку!", ephemeral=True)
    @discord.ui.button(label="Принять", style=discord.ButtonStyle.green, custom_id="ticket_button_consideration", emoji="✅")
    @app_commands.checks.has_permissions(administrator=True)
    async def consideration_ticket(self, interaction: discord.Interaction, button: discord.ui.button):
        try:
            await check_user(id=interaction.user.id, user_name=interaction.user.name)
            user = dbMaria.get_data_by_condition(condition_column='user_id', table_name='users', condition_value=interaction.user.id); user = user[0]
            self.plus_button_clicked_by_user = True
            ticket_data = dbMaria.get_data_by_condition(condition_column='message_id', condition_value=interaction.message.id, table_name='tickets')
            if ticket_data == []:
                return await interaction.response.send_message("Тикет не найден!", ephemeral=True)
            ticket_data = ticket_data[0]
            user_assignment = dbMaria.get_data_by_condition(condition_column='ticket_id', condition_value=ticket_data['ticket_id'], table_name='assigned_tickets')
            if user_assignment == []:
                await interaction.response.send_message("Вам будет присвоен новый тикет!", ephemeral=True)
                channel_id = int(ticket_data['channel_id'])
                channel = interaction.guild.get_channel(channel_id)
                await channel.set_permissions(interaction.user, read_messages=True, view_channel=True, send_messages=True, embed_links= True, read_message_history = True)
                if channel:
                    embed_control = discord.Embed(title="Тикет рассматривается", description=f"Куратор: <@{interaction.user.id}> канал: {interaction.channel.mention}", color=discord.Colour.dark_grey())
                    assigned_message = await interaction.user.send(embed=embed_control, view=control_ticket_system_users()) # view=buttons_control_ticket()
                    dbMaria.insert_assignment(assigned_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ticket_id=ticket_data['ticket_id'], user_id=interaction.user.id, assignment_id=assigned_message.id)
                    print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}accept ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
                else:
                    print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}channel not found: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
            else:
                return await interaction.response.send_message("Тикет уже забрали!")
        except Exception as e:
            print(f"Error touch button: {e}")
            return await interaction.response.send_message("Ошибка при нажатии на кнопку!", ephemeral=True)

client_control = None
class control_ticket_system_users(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Закрыть тикет!", style=discord.ButtonStyle.red, custom_id="control_system_ticket_close", emoji="🧨")
    async def close_ticket_user(self, interaction: discord.Interaction, button: discord.ui.button):
        user = dbMaria.get_data_by_condition(condition_column='assignment_id', condition_value=interaction.message.id, table_name='assigned_tickets'); user = user[0]
        if user:
            channel_data = dbMaria.get_data_by_condition(condition_column='ticket_id', condition_value=user['ticket_id'], table_name='tickets'); channel_data = channel_data[0]
            if channel_data['channel_id'] == None:
                return await interaction.response.send_message("Тикет не найден!", ephemeral=True)
            dbMaria.delete_one_data(table_name="assigned_tickets",condition_column="ticket_id",condition_value=channel_data['ticket_id'])
            dbMaria.delete_one_data(table_name="tickets",condition_column="ticket_id",condition_value=channel_data['ticket_id'])
            await client_control.client.get_channel(int(channel_data['channel_id'])).delete()
            await interaction.message.delete()
            await interaction.response.send_message(f"Тикет закрыт!", ephemeral=True)
            print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}close ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        else:
            await interaction.response.send_message(f"Нету информации о тикете!", ephemeral=True)
    @discord.ui.button(label="Информация о тикете", style=discord.ButtonStyle.grey, custom_id="control_system_ticket_info", emoji="🧮")
    async def info_ticket_user(self, interaction: discord.Interaction, button: discord.ui.button):
        user = dbMaria.get_data_by_condition(condition_column='assignment_id', condition_value=interaction.message.id, table_name='assigned_tickets'); user = user[0]
        if user:
            channel_data = dbMaria.get_data_by_condition(condition_column='ticket_id', condition_value=user['ticket_id'], table_name='tickets'); channel_data = channel_data[0]
            if channel_data['channel_id'] == None:
                return await interaction.response.send_message("Тикет не найден!", ephemeral=True)
            Embed = discord.Embed(title='📓 ⭑ Информация о тикете', description="""""", color=0xffffff)
            await interaction.response.send_message(embed=Embed, ephemeral=True)
        else:
            await interaction.response.send_message(f"Нету информации о тикете!", ephemeral=True)


"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    global client_control
    try:
        client_control = ticket_system_report(client)
        client.add_view(control_ticket_system_users())
        client.add_view(buttons_on_control_ticket_by_moderator())
        client.add_view(create_ticket_reports())
        await client.add_cog(ticket_system_report(client), guilds=[discord.Object(id=1200955239281467422)])
        print(f"{Fore.GREEN}Cog '{Fore.RED}ticket_report{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}ticket_report{Fore.GREEN}': {e}{Style.RESET_ALL}")
