import os
import sys
import discord
from discord import app_commands
from dotenv import load_dotenv
import importlib
# Устанавливаем текущую директорию на директорию скрипта
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

# Добавляем 'app' в sys.path
app_directory = os.path.join(current_directory, 'app')
sys.path.append(app_directory)

load_dotenv()
BOT_TICKETS = os.getenv('BOT_TICKETS')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

async def load_commands():
    # Используем относительный путь к папке с командами относительно main.py
    commands_folder = os.path.join(current_directory, '..', 'commands')
    for filename in os.listdir(commands_folder):
        if filename.startswith('tickets_') and filename.endswith('.py'):
            module_name = filename[:-3]  # remove the '.py' extension
            module_path = os.path.join(commands_folder, filename)
            try:
                spec = importlib.util.spec_from_file_location(f'app.commands.{module_name}', module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if callable(attribute) and hasattr(attribute, 'slash_command'):
                        tree.add_command(attribute)
                        print(f"Loaded command: {attribute_name}")

            except Exception as e:
                print(f"Failed to load extension {filename}.", e)

@client.event
async def on_ready():
    await load_commands()
    await tree.sync()
    print("Ready!")

@tree.command(
    name="tickets",
    description="create ticket and ...",
)
async def first_command(interaction):
    try:
        await interaction.response.send_message("Nothing settings on command")
    except Exception as e:
        await interaction.response.send_message("An error occurred:", e)

client.run(BOT_TICKETS)
