from discord.ext import commands
import discord

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Добавляем вид кнопки для создания тикета
        await self.bot.add_view(TicketView())

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Создать тикет", style=discord.ButtonStyle.red, custom_id="Ticket Button")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Проверяем, существует ли уже тикет для пользователя
        ticket = discord.utils.get(interaction.guild.text_channels, name=f"ticket-player-{interaction.user.name}-{interaction.user.discriminator}")
        if ticket is not None: await interaction.response.send_message(f"У тебя уже открыт тикет на {ticket.mention}!")
        else:
            # Создаем разрешения для канала тикета
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                self.bot.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            }

            # Создаем канал тикета
            channel = await interaction.guild.create_text_channel(name=f"ticket-player-{interaction.user.name}-{interaction.user.discriminator}", overwrites=overwrites, reason=f"Ticker for {interaction.user}")

            # Создаем и отправляем приветственное сообщение в канал
            embed = discord.Embed(title="Добро пожаловать в твой тикет!", description="Здесь ты можешь описать свою проблему. Модераторы скоро ответят тебе.")
            await channel.send(embed=embed)

            # Отправляем сообщение-ответ пользователю
            await interaction.response.send_message(f"Я создал для тебя тикет на {channel.mention}. Модераторы ответят тебе как можно скорее!", ephemeral=True)

    @discord.ui.button(label="Закрыть тикет", style=discord.ButtonStyle.red, custom_id="Close Button")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Проверяем, находится ли пользователь в канале тикета
        if "ticket-player-" not in interaction.channel.name:
            await interaction.response.send_message("Это не тикет!", ephemeral=True)
            return

        # Подтверждение закрытия тикета
        embed = discord.Embed(title="Вы уверены, что хотите закрыть этот тикет?", color=discord.Colour.blurple())
        await interaction.response.send_message(embed=embed, view=ConfirmView(), ephemeral=True)

class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Да", style=discord.ButtonStyle.green, custom_id="Confirm Yes")
    async def confirm_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Удаляем канал тикета
        await interaction.channel.delete()
        await interaction.response.send_message("Тикет закрыт.", ephemeral=True)

    @discord.ui.button(label="Нет", style=discord.ButtonStyle.red, custom_id="Confirm No")
    async def confirm_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Закрытие тикета отменено.", ephemeral=True)

