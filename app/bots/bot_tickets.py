import discord
from discord import File
from discord.ext import commands
from colorama import Back, Fore, Style
import logging
import time
import platform
import cogs.database.database as dbMaria
from easy_pil import Editor, load_image_async, Font
from dispie import EmbedCreator
# from dispie import EmbedCreator
from config import Bot_tickets, tickets_cogs

class CustomLogging():
    logger: logging
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
    def log(self, message):
        self.logger.info(message)
print = CustomLogging().log

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
        self.cogslist = ["cogs.ticket_system", "cogs.add_role_system", "cogs.ember_creator_system"]
        # self.synced = False #we use this so the bot doesn't sync commands more than once
        # self.added = False
    async def setup_hook(self) -> None:
        for ext in self.cogslist:
            await self.load_extension(ext)
        # if not self.added:
        #     self.add_view(ticket_launcher())
        #     self.add_view(main())
        #     self.added = True

    async def on_ready(self):
        try:
            await self.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='twinsikk', url='https://www.twitch.tv/twinsikk'))
            prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
            print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
            print(prfx + " ID: " + Fore.YELLOW + str(self.user.id))
            print(prfx + " Version: " + Fore.YELLOW + str(discord.__version__))
            print(prfx + " Platform: " + Fore.YELLOW + platform.system())
            print(prfx + " Python: " + Fore.YELLOW + platform.python_version())
            print(prfx + " Discord.py: " + Fore.YELLOW + discord.__version__)
            print(prfx + " Bot: " + Fore.YELLOW + "Bot_tickets")
            print(f"{Fore.GREEN}Бот {self.user} запущен!{Style.RESET_ALL}")
            print(f'Вошёл как {self.user} (ID: {self.user.id})')
            await self.tree.sync()
            await self.setup_hook()
            # if not self.added:
            #     self.add_view(ticket_launcher())
            #     self.add_view(main())
            #     self.added = True
        except Exception as e:
            print(f"{Fore.RED}Error logging in as {self.user}: {e}{Style.RESET_ALL}")

# def has_specific_roles(*role_ids):
#     async def predicate(ctx):
#         user_roles = [role.id for role in ctx.author.roles]
#         return any(role_id in user_roles for role_id in role_ids)
#     return commands.check(predicate)

# MariaDB Save-all roles on guild
# Пример вставки данных
# data_to_insert = {'user_id': '123', 'image': b'\x89PNG\r\n\x1a\n...', 'text_message': 'Hello, World!'}
# db_manager.insert_data('new_table', data_to_insert)


Client = Client()
# Command's next
"""
Slash Commands Next: //
help
"""
@Client.tree.command(name="embed", description="embed")
async def embed(interaction: discord.Interaction):
    view = EmbedCreator(bot=Client)
    await interaction.response.send_message(embed=view.get_default_embed, view=view)
# @Client.tree.command(name="create-database", description="Создание таблицы в базе-данных")
# @commands.has_permissions(administrator=True)
# async def save_image(interaction: discord.Interaction):
#     await interaction.response.send_message(f'Создание таблицы в базе-данных')
#     db_manager = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
#     columns = {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'user_id': 'VARCHAR(255)', 'image': 'BLOB', 'text_message': 'TEXT'}
#     db_manager.create_table('new_table', columns)


# @Client.tree.command(name="execute-sql", description="admin")
# async def command_permissions(interaction: discord.Interaction):
#     await interaction.response.send_message(f'Даем разрешение на команду')
#     db_manager = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
#     db_manager.execute_all_sql_files_in_subfolder('sql-data')


# @Client.tree.command(name="save-roles", description="Сохранение ролей")
# @commands.has_permissions(administrator=True)
# async def save_roles(interaction: discord.Interaction):
#     guild = interaction.guild
#     db_manager = dbMaria.MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
#     db_manager.delete_all_data('roles')
#     for role in guild.roles:
#         db_manager.insert_data('roles', data={'role_id': str(role.id), 'role_name': role.name})
#     await interaction.response.send_message("Роли сохранены в базе данных.")


# @Client.tree.command(name="get-guilds", description="Displays information about the bot's guilds")
# async def get_guilds(interaction: discord.Interaction):
#     # Check if the bot has the 'View Members' permission in the current guild
#     if not (await commands.member_has_permissions(interaction.guild, interaction.user, view_members=True)):
#         await interaction.response.send_message("I don't have permission to view guild members! Please grant me the 'View Members' permission.")
#         return

"""
Events Next: //
on_ready,
on_member_join, 
on_member_remove, 
on_member_update, 
on_message, 
on_typing, 
on_voice_state_update, 
on_webhooks_update,
on_message_delete, 
on_message_edit, 
on_reaction_add, 
on_reaction_remove, 
on_raw_reaction_add, 
on_raw_reaction_remove
on_raw_message_delete,
on_raw_message_edit,
on_raw_reaction_clear,
on_raw_reaction_clear_emoji,
on_guild_join,
on_guild_remove,
on_guild_update,
on_guild_role_create,
on_guild_role_delete,
on_guild_role_update,
on_guild_emojis_update,
on_guild_stickers_update,
on_guild_integrations_update,
on_application_command_error,
on_application_command_create,
on_application_command_update,
on_application_command_delete,
on_button_click,
on_select_option,
on_autocomplete,
on_modal_submit,
on_modal_submit,
on_scheduled_event_create,
on_scheduled_event_update,
on_scheduled_event_delete,
on_scheduled_event_user_add,
"""

@Client.event
# ---------------------------------------------
async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(1214952893271248946)
    
    background = Editor('app/bots/Reports-banner.png')
    profile_image = await load_image_async(str(member.avatar.url))
    
    profile = Editor(profile_image).resize((150, 150)).circle_image()
    popping = Font.poppins(size=50, variant="bold")
    poppins_small = Font.poppins(size=20, variant="light")
    
    background.paste(profile, (325, 90))
    background.ellipse((325, 90), 150, 150, outline=None, stroke_width=5)
    
    background.text((450, 160), member.name, color="white", font=popping)
    background.text((450, 200), str(member.id), color="white", font=poppins_small)  # Convert member.id to string
    
    file = File(fp=background.image_bytes, filename="https://i.imgur.com/8txHSse.png")
    await channel.send(file=file)

    try:
        channel = member.guild.get_channel(1207710865202221076)
        if channel:
            await channel.send(f'```Индентификатор:{member.id}``` ```Имя пользователя:{member.name}``` ```Присоединился:{member.joined_at}``` Аватар:{member.avatar}!')
            role = member.guild.get_role(1204254987396448287)
            if role:
                await member.add_roles(role)
                print(f'Участнику {member.name} присвоена роль {role.name}.')
            else:
                print('Указанная роль не найдена.')
        else:
            print('Указанный канал не найден.')
    except Exception as e:
        print(f'Ошибка при обработке события on_member_join: {e}')
# ---------------------------------------------
@Client.event
async def message_event(member: discord.Member):
    try:
        channel = member.guild.get_channel(1207710865202221076)
        if channel:
            await channel.send(f'```Индентификатор:{member.id}``` ```Имя пользователя:{member.name}``` ```Присоединился:{member.joined_at}``` Аватар:{member.avatar}!')
            role = member.guild.get_role(1204254987396448287)
            if role:
                await member.add_roles(role)
                print(f'Участнику {member.name} присвоена роль {role.name}.')
            else:
                print('Указанная роль не найдена.')
        else:
            print('Указанный канал не найден.')
    except Exception as e: discord.message
@Client.event
async def on_guild_join(guild: discord.Guild):
    print(f"Бот присоединился к серверу {guild.name} (ID: {guild.id})")
    print(f"Количество участников: {len(guild.members)}")
    print(f"Количество каналов: {len(guild.channels)}")
    print(f"Количество ролей: {len(guild.roles)}")
#  ========================
"""Start Client"""
Client.run(Bot_tickets)
"""
Bot_tickets = {Token.bot}
"""
#  ========================