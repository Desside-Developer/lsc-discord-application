import discord
import logging

from discord import app_commands, utils
from discord.ui import View, Button
from discord.ext import commands
from colorama import Back, Fore, Style

from database.database import dbMaria
from handlers.hand_package import check_user, check_user_tags, save_user_tags, check_name_second
from logs.logging import logs_responde

print = logging.info

class system_start(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    @commands.command(name="test01")
    @commands.has_permissions(administrator=True)
    async def system_messages(self, ctx: commands.Context):
        await ctx.message.delete()
        embed = discord.Embed(color=0x000001, title="Добро пожаловать на сервер!", description="""
1. Вам __необходимо__ пройти **мини**-``авторизацию``
Нажмите на ``кнопку`` авторизации
и введите свой никнейм из проекта ``Arizona``.
**Вам сгенерируем, уникальный айди** ``[0000]``
Данная регистрация проходит единожды, но если
вы покинете наш сервер, ваш пользователь будет анулирован.
""")
        view = system_start_view()
        await ctx.send(embed=embed, view=view)






class system_start_view(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Авторизация", style=discord.ButtonStyle.gray, custom_id="system_start_button_auth", emoji="🌎")
    async def system_start_button_authorization(self, interaction: discord.Interaction, button: discord.ui.Button):
        # search_user = dbMaria.get_data_by_condition('users', condition_column='user_id',condition_value=interaction.user.id)
        await check_user(id=interaction.user.id, user_name=interaction.user.name)
        search_user_tags = await check_user_tags(id=interaction.user.id)
        if search_user_tags == False:
            modal_windows = await interaction.response.send_modal(modal_window_replace_name())
        else:
            await interaction.response.send_message("Вы уже авторизованы!", ephemeral=True)
@app_commands.describe(name="Ваше имя:", second="Ваша фамилия:")
class modal_window_replace_name(discord.ui.Modal, title="📌🞄 заполните пункты"):
    name = discord.ui.TextInput(label="Ваше имя:", placeholder="пример: John", style=discord.TextStyle.paragraph)
    second = discord.ui.TextInput(label="Ваша фамилия:", placeholder="пример: William", style=discord.TextStyle.paragraph)
    async def on_submit(self, interaction: discord.Interaction):
        name_second = f"{self.name.value} {self.second.value}"
        name_second_response = await check_name_second(name_second=name_second)
        if name_second_response == True:
            return await interaction.response.send_message("Такое имя уже есть!", ephemeral=True)
        user_data = await save_user_tags(id=interaction.user.id, name_second=name_second)
        await logs_responde.auth_users(dict=user_data)
        print(f"""
{Fore.RED}( System_Auth )
user_id: {user_data['user_id']}
unique_id: {user_data['unique_id']}
username: {user_data['username']}
balance: {user_data['balance']}
on_joined: {user_data['on_joined']}
inventory: {user_data['inventory']}
""")
        try:
            user = await interaction.guild.fetch_member(interaction.user.id)
            await user.edit(nick=f"{user_data['unique_id']} {name_second}")
            await interaction.user.add_roles(interaction.guild.get_role(1204255081147666492))
            await interaction.response.send_message("Регистрация завершена!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(e, ephemeral=True)


"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [system_start]
    for cog in cogs:
        try:
            await client.add_cog(cog(client), guilds=[discord.Object(id=1200955239281467422)])
            client.add_view(system_start_view())
            print(f"{Fore.GREEN}Cog '{Fore.RED}system_start{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}system_start{Fore.GREEN}': {e}{Style.RESET_ALL}")
