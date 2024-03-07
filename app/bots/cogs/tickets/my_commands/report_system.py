from colorama import Fore
from discord.ui import View, Button
from discord import app_commands, utils
import discord

import config # Импортируем конфиг файл для доступа к ключам и значениям

# --------------------------------------------------------------------------------------------------------------------------------
# Кнопка для создания тикета для репортов
# --------------------------------------------------------------------------------------------------------------------------------
class button_create_ticket_report(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(label="Создать тикет", style=discord.ButtonStyle.green, custom_id="ticket_button_report", emoji="🎟"))
    @app_commands.checks.has_permissions(send_messages=True)
    async def button_create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal_windows = await interaction.response.send_modal(modal_window_ticket_system_report())
        if modal_windows is None:
            print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")
        else:
            await modal_windows.delete()
# --------------------------------------------------------------------------------------------------------------------------------  
      
# --------------------------------------------------------------------------------------------------------------------------------
# Модальное окно для вывода ошибок и запросов от пользователя для создания тикета для репортов
# --------------------------------------------------------------------------------------------------------------------------------
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
        embed_ticket_player = discord.Embed(title=f"Тикет ID:``{interaction.user.id}``", description=f"{interaction.user.mention} Вы создали свой тикет!", color= discord.Colour.blue())
        embed_ticket_player.add_field(name=f"Проблема", value=f"{self.problem}", inline=True)
        embed_ticket_player.add_field(name=f"Подробное описание", value=f"{self.description_problem}", inline=False)
        message_id = await channel.send(embed=embed_ticket_player)
        await interaction.response.send_message("Тикет создан!", ephemeral=True)
# --------------------------------------------------------------------------------------------------------------------------------