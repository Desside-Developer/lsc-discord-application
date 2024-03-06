# import multiprocessing
# import os
import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from app.bots.config import Bot_tickets
import time
import json
import platform

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=discord.Intents.all())
        self.cogslist = ["items"]
    async def setup_hook(self) -> None:
        for ext in self.cogslist:
            await self.load_extension(ext)
        # self.load_extension("app.bots.bot_tickets")
        # self.load_extension("app.bots.bot_music")
        # self.load_extension("app.bots.bot_moderator")
        # self.load_extension("app.bots.bot_test")

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " ID: " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Version: " + Fore.YELLOW + str(discord.__version__))
        print(prfx + " Platform: " + Fore.YELLOW + platform.system())
        print(prfx + " Python: " + Fore.YELLOW + platform.python_version())
        print(prfx + " Discord.py: " + Fore.YELLOW + discord.__version__)
        print(prfx + " Bot: " + Fore.YELLOW + "Bot_tickets")
        print(f"{Fore.GREEN}Бот {self.user} запущен!{Style.RESET_ALL}")
        await self.tree.sync()
        

Client = Client()
@Client.tree.command(name="modal", description="modalWindows")
async def modal(interaction: discord.Interaction):
    modal = discord.ui.Modal(title="modal")
    modal.add_item(discord.ui.InputText(label="text", placeholder="text"))
    await interaction.response.send_modal(modal)
Client.run(Bot_tickets)

# def run_bot(token):
#     os.system(f"python {token}.py")


# if __name__ == "__main__":
#     bot_tokens = ['app\\bots\\bot_tickets', 'app\\bots\\bot_music', 'app\\bots\\bot_moderator']
#     processes = []
#     for token in bot_tokens:
#         p = multiprocessing.Process(target=run_bot, args=(token,))
#         processes.append(p)
#         p.start()
#     for process in processes:
#         process.join()