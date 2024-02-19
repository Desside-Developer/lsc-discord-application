#!/usr/bin/env python3

from discord.ext import commands
import discord
from discord import app_commands
from dispie import EmbedCreator
from app.bots.config import Bot_tickets, tickets_cogs

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
        # await interaction.channel.delete(reason="Ticket closed by user")
        # await interaction.response.send_message("Ticket closed!", ephemeral=True)
        # self.stop()
        # return

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents, **kwargs)
        self.synced = False #we use this so the bot doesn't sync commands more than once
        self.added = False

    async def setup_hook(self):
        for cog in tickets_cogs:
            try:
                await self.load_extension(cog)
            except Exception as exc:
                print(f'Не удалось загрузить расширение {cog} из-за {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        print(f'Вошёл как {self.user} (ID: {self.user.id})')
        await self.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='twinsikk', url='https://www.twitch.tv/twinsikk'))
        await self.tree.sync()
        if not self.added:
            self.add_view(ticket_launcher())
            self.add_view(main())
            self.added = True

def has_specific_roles(*role_ids):
    async def predicate(ctx):
        user_roles = [role.id for role in ctx.author.roles]
        return any(role_id in user_roles for role_id in role_ids)
    return commands.check(predicate)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True
intents.reactions = True
bot = Bot(intents=intents)

def has_at_least_one_required_role(required_role_ids):
    async def predicate(interaction: discord.Interaction):
        for role_id in required_role_ids:
            if role_id in [role.id for role in interaction.user.roles]:
                return True
        await interaction.response.send_message("У вас недостаточно прав для использования этой команды.", ephemeral=True)
        return False
    return discord.app_commands.checks.check(predicate)
def has_required_role_and_send_error(required_role_id):
    async def predicate(interaction: discord.Interaction):
        if required_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("У вас недостаточно прав для использования этой команды.", ephemeral=True)
            return False
        return True
    return discord.app_commands.checks.check(predicate)


@bot.event
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

# write general commands here
@bot.tree.command(name="create-embed", description="Создание Embed сообщений!")
@has_at_least_one_required_role([1204254973542793237])
async def create_embed(interaction: discord.Interaction):
    view = EmbedCreator(bot=bot)
    await interaction.response.send_message(embed=view.get_default_embed, view=view)


@bot.tree.command(name='ticket', description='Запускает систему билетов (@)')   # guilds=discord.Object(id='1200955239281467422')
@has_required_role_and_send_error(1204254973542793237)
async def ticketing(interaction: discord.Interaction):
    embed = discord.Embed(title="Нажмите кнопку ниже и создайте заявку!", color=discord.Colour.orange())
    await interaction.channel.send(embed=embed, view=ticket_launcher())
    await interaction.response.send_message("Запущена система тикетов!", ephemeral=True)

@bot.tree.command(name='close', description='Закрывает Тикет')
@has_required_role_and_send_error(1204254973542793237)
async def close(interaction: discord.Interaction):
    if "тикет-игрока-" in interaction.channel.name:
        embed = discord.Embed(title="Вы уверены, что хотите закрыть этот тикет?", color=discord.Colour.blurple())
        await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True) # view=self
    else: await interaction.response.send_message("Это не тикет!", ephemeral=True)
    
@bot.tree.command(name='add', description='Добавляет пользователя в тикет')
@app_commands.describe(user="Пользователь, которого вы хотите добавить")
@has_required_role_and_send_error(1204254973542793237)
async def add(interaction: discord.Interaction, user: discord.Member):
    if "ticket-for-" in interaction.channel.name:
        await interaction.channel.set_permissions(user, view_channel=True, send_messages=True, attach_files=True, embed_links=True)
        await interaction.response.send_message(f"{user.mention} был добавлен в билет пользователем {interaction.user.mention}!", ephemeral=True)
    else: await interaction.response.send_message("Это не тикет!", ephemeral=True)
    
bot.run(Bot_tickets)
