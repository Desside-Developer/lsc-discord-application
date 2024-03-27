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


class on_reaction_embed(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.roles = {
            "<a:8356873:1222315483379007568>": 1204254987396448287,
            "<a:6234623:1222315506455937146>": 1204254984581939251,
        }
    @commands.command(name="embed-reactions")
    @commands.has_permissions(administrator=True)
    async def embed_reactions(self, ctx: commands.Context):
        await ctx.message.delete()
        embed = discord.Embed(color=0x000001, title="📌 ⭑ Нажмите на реакцию для того чтобы получить роль!", description=f"""
1. **LSC Client** - <a:8356873:1222315483379007568>
2. **Arenda Client** - <a:6234623:1222315506455937146>
        """)
        embed.set_image(url="https://i.imgur.com/2TdAVOz.jpeg")
        embed.set_footer(text="𝐋𝐒𝐂 - 𝙎𝙚𝙧𝙫𝙞𝙘𝙚𝙨  [✅]")
        message = await ctx.send(embed=embed) 
        for emoji in self.roles.keys():
            await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 1222516217269584023:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            emoji_name = str(payload.emoji)

            if emoji_name in self.roles.keys():
                role_id = self.roles[emoji_name]
                role = guild.get_role(role_id)
                if role:
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 1222516217269584023:
            guild = self.client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            emoji_name = str(payload.emoji)

            if emoji_name in self.roles.keys():
                role_id = self.roles[emoji_name]
                role = guild.get_role(role_id)
                if role:
                    await member.remove_roles(role)

"""
- Setup Cogs ->
"""
async def setup(client: commands.Bot) -> None:
    cogs = [on_reaction_embed]
    for cog in cogs:
        try:
            await client.add_cog(cog(client), guilds=[discord.Object(id=1200955239281467422)])
            client.add_view(cog())
            print(f"{Fore.GREEN}Cog '{Fore.RED}on_reaction_embed{Fore.GREEN}' successfully added.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error adding cog '{Fore.RED}on_reaction_embed{Fore.GREEN}': {e}{Style.RESET_ALL}")
