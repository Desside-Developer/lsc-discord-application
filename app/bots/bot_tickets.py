import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import logging
import time
import platform
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
        self.cogslist = ["cogs.ticket_system"]
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
            # await self.tree.sync()
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

Client = Client()
# Command's next



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
#  ========================
"""Start Client"""
Client.run(Bot_tickets)
"""
Bot_tickets = {Token.bot}
"""
#  ========================