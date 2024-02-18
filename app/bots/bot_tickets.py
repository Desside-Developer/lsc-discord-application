#!/usr/bin/env python3

from discord.ext import commands
from dispie import EmbedCreator
import discord
from config import Bot_tickets, tickets_cogs
from discord import app_commands

class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.blurple, custom_id="Ticket Button")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = discord.utils.get(interaction.guild.text_channels, name=f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}")
        if ticket is not None: await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!", ephemeral=True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
            }
            channel = await interaction.guild.create_text_channel(name=f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}", overwrites=overwrites, reason=f"Ticket for {interaction.user}")
            await channel.send(f"{interaction.user.mention} Created a ticket!", view= main())
            await interaction.response.send_message(f"I've opened a ticket for you at {channel.mention}!", ephemeral=True)

class confirm(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red, custom_id="Confirm")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try: await interaction.channel.delete(reason="Ticket closed by user")
        except: await interaction.response.send_message("Channel deletion failed! Make sure i have 'manage_channels' permissions", ephemeral=True)
class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="Close")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Are you sure you want to close this ticket?", color=discord.Colour.blurple())
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
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {exc}')

    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')
        await self.tree.sync()
        if not self.added:
            self.add_view(ticket_launcher())
            self.add_view(main())
            self.added = True


intents = discord.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)


# write general commands here
@bot.tree.command(name="create-embed", description="embed..")
async def create_embed(interaction: discord.Interaction):
    view = EmbedCreator(bot=bot)
    await interaction.response.send_message(embed=view.get_default_embed, view=view)


@bot.tree.command(name='ticket', description='Launches the ticketing system')   # guilds=discord.Object(id='1200955239281467422')
async def ticketing(interaction: discord.Interaction):
    embed = discord.Embed(title="If you need support, click the button below and create a ticket!", color=discord.Colour.blue())
    await interaction.channel.send(embed=embed, view=ticket_launcher())
    await interaction.response.send_message("Ticketing system launched!", ephemeral=True)

@bot.tree.command(name='close', description='Closes the ticket')
async def close(interaction: discord.Interaction):
    if "ticket-for-" in interaction.channel.name:
        embed = discord.Embed(title="Are you sure you want to close this ticket?", color=discord.Colour.blurple())
        await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True) # view=self
    else: await interaction.response.send_message("This is not a ticket!", ephemeral=True)
    
@bot.tree.command(name='add', description='Adds a user to the ticket')
@app_commands.describe(user="The user you want to add")
async def add(interaction: discord.Interaction, user: discord.Member):
    if "ticket-for-" in interaction.channel.name:
        await interaction.channel.set_permissions(user, view_channel=True, send_messages=True, attach_files=True, embed_links=True)
        await interaction.response.send_message(f"{user.mention} has been added to the ticket by {interaction.user.mention}!", ephemeral=True)
    else: await interaction.response.send_message("This is not a ticket!", ephemeral=True)
    
bot.run(Bot_tickets)
