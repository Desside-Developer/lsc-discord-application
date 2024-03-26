import datetime
import discord
import json
from discord.ext import commands
from colorama import Back, Fore, Style
from discord import app_commands, utils
from discord.ui import View, Button
from database.database import dbMaria
import config 
import logging
print = logging.info

class tickets_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ticket-system-report", description="Система тикетов для > Репортов")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_system_report(self, interaction: discord.Interaction):
        
        embed = discord.Embed(title="📌🞄 Создайте тикет для - Репортов!", description="Нажмите на кнопку чтобы создать тикет", color=0xffffff)
        embed.set_author(name=f"{config.ticket_system_author}")
        embed.set_footer(text="``Статус тикетов: Работает``")
        
        # view = create_ticket_reports()
        
        # await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Тикет создан!", ephemeral=True)
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_report{Fore.RESET}")

    @app_commands.command(name="ticket-system-set", description="Система тикетов для > Настройка Авто")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_system_set(self, interaction: discord.Interaction):
        embed = discord.Embed(title="⏰🞄 Создайте тикет для - Настройки Авто!", description="Нажмите на кнопку чтобы создать тикет", color=0x9bb8a0)
        embed.set_author(name=f"{config.ticket_system_author}")
        embed.set_footer(text="``Статус тикетов: Работает``")

        # view = create_ticket_cheap()

        # await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Тикет создан!", ephemeral=True)

        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_set{Fore.RESET}")
    @app_commands.command(name="ticket-system-rep", description="Система тикетов для > Починки Двигателя")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_system_rep(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🔧🞄 Создайте тикет для - Починки Двигателя!", description="Нажмите на кнопку чтобы создать тикет", color=0xff0044)
        embed.set_author(name=f"{config.ticket_system_author}")
        embed.set_footer(text="``Статус тикетов: Работает``")

        # view = create_ticket_cheap()

        # await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Тикет создан!", ephemeral=True)

        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_rep{Fore.RESET}")
    @app_commands.command(name="ticket-system-rent", description="Система тикетов для > Аренда Авто")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_system_rent(self, interaction: discord.Interaction):
        embed = discord.Embed(title="💼🞄 Создайте тикет для - Аренда Авто!", description="Нажмите на кнопку чтобы создать тикет", color=0xe6ca00)
        embed.set_author(name=f"{config.ticket_system_author}")
        embed.set_footer(text="``Статус тикетов: Работает``")

        # view = create_ticket_cheap()

        # await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Тикет создан!", ephemeral=True)

        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_rent{Fore.RESET}")
    @app_commands.command(name="ticket-system-feedback", description="Система тикетов для > Feedbacks")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_system_feedback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="📝🞄 Создайте тикет для - Feedbacks!", description="Нажмите на кнопку чтобы создать тикет", color=0x27ff78)
        embed.set_author(name=f"{config.ticket_system_author}")
        embed.set_footer(text="``Статус тикетов: Работает``")

        # view = create_ticket_cheap()

        # await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("Тикет создан!", ephemeral=True)

        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}created ticket system: {Fore.GREEN}ticket_system_feedback{Fore.RESET}")
    @app_commands.command(name="close", description="delete-ticket")
    @app_commands.checks.has_permissions(move_members=True)
    async def ticket_delete(self, interaction: discord.Interaction,):
        await interaction.channel.delete()
        await interaction.response.send_message("Тикет удален!", ephemeral=True)
        print(f"{Fore.RED}{interaction.user} {Fore.YELLOW}deleted ticket: {Fore.GREEN}Ticket-System-001{Fore.RESET}")


"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [tickets_system]
    for cog in cogs:
        try:
            # client.add_view(control_ticket_system_users())
            # client.add_view(buttons_on_control_ticket_by_moderator())
            # client.add_view(create_ticket_cheap())
            # client.add_view(create_ticket_reports())
            await client.add_cog(cog(client))
            print(f"{Fore.GREEN}Cog '{Fore.RED}{cog}{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}{cog}{Fore.GREEN}': {e}{Style.RESET_ALL}")
