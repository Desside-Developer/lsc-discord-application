import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands
import logging

# class CustomLogging():
#     logger: logging
#     def __init__(self):
#         self.logger = logging.getLogger()
#         self.logger.setLevel(logging.INFO)
#         self.logger.addHandler(logging.StreamHandler())
#     def log(self, message):
#         self.logger.info(message)
print = logging.info
# from service.check_role import check_role_on_user as check_role

class tickets_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @app_commands.command(name="ticket", description="Создать тикет")
    async def ticketing(interaction: discord.Interaction):
        embed = discord.Embed(title="Нажмите кнопку ниже и создайте заявку!", color=discord.Colour.orange())
        await interaction.channel.send(embed=embed, view=ticket_launcher) # ticket_launcher()
        await interaction.response.send_message("Запущена система тикетов!", ephemeral=True)

class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @discord.ui.button(label="Кликай чтобы создать тикет!", style=discord.ButtonStyle.green, custom_id="Ticket Button")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = discord.utils.get(interaction.guild.text_channels, name=f"тикет-игрока-{interaction.user.name}-{interaction.user.discriminator}")
        if ticket is not None: await interaction.response.send_message(f"У вас уже открыт тикет на {ticket.mention}!", ephemeral=True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
            }
            channel = await interaction.guild.create_text_channel(name=f"тикет-игрока-{interaction.user.name}-{interaction.user.discriminator}", overwrites=overwrites, reason=f"Ticket for {interaction.user}")
            await channel.send(f"<@&{1204255066869989437}>, {interaction.user.mention} Здраствуйте, пишите свое мнение о нас!", view= main())
            await interaction.response.send_message(f"Я открыл для тебя тикет на {channel.mention}!", ephemeral=True)

class confirm(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Потвердить", style=discord.ButtonStyle.red, custom_id="Confirm")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try: await interaction.channel.delete(reason="Заявка закрыта пользователем")
        except: await interaction.response.send_message("Удаление канала не удалось! Убедитесь, что у меня есть 'manage_channels' права", ephemeral=True)

class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="Close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Вы уверены, что хотите закрыть этот тикет?", color=discord.Colour.blurple())
        await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True) # view=self
        await interaction.channel.delete(reason="Ticket closed by user")
        await interaction.response.send_message("Ticket closed!", ephemeral=True)
        self.stop()
        return
        
# write general commands here  
# @has_at_least_one_required_role([1204254973542793237])


# @bot.tree.command(name='tickets', description='Запускает систему билетов (@)')   # guilds=discord.Object(id='1200955239281467422')
# @has_required_role_and_send_error(1204254973542793237)
# async def ticketing(interaction: discord.Interaction):
#     embed = discord.Embed(title="Нажмите кнопку ниже и создайте заявку!", color=discord.Colour.orange())
#     # from __init__ import ticket_launcher_discord
#     await interaction.channel.send(embed=embed) # ticket_launcher()
#     await interaction.response.send_message("Запущена система тикетов!", ephemeral=True)

# @bot.tree.command(name='close', description='Закрывает Тикет')
# @has_required_role_and_send_error(1204254973542793237)
# async def close(interaction: discord.Interaction):
#     if "тикет-игрока-" in interaction.channel.name:
#         embed = discord.Embed(title="Вы уверены, что хотите закрыть этот тикет?", color=discord.Colour.blurple())
#         await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True) # view=self
#     else: await interaction.response.send_message("Это не тикет!", ephemeral=True)
    
# @bot.tree.command(name='add', description='Добавляет пользователя в тикет')
# @app_commands.describe(user="Пользователь, которого вы хотите добавить")
# @has_required_role_and_send_error(1204254973542793237)
# async def add(interaction: discord.Interaction, user: discord.Member):
#     if "ticket-for-" in interaction.channel.name:
#         await interaction.channel.set_permissions(user, view_channel=True, send_messages=True, attach_files=True, embed_links=True)
#         await interaction.response.send_message(f"{user.mention} был добавлен в билет пользователем {interaction.user.mention}!", ephemeral=True)
#     else: await interaction.response.send_message("Это не тикет!", ephemeral=True)

"""
 - Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    try:
        await client.add_cog(tickets_system(client))
        print(f"{Fore.GREEN}Cog '{Fore.RED}{tickets_system}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error adding cog '{Fore.RED}{tickets_system}{Fore.GREEN}': {e}{Style.RESET_ALL}")