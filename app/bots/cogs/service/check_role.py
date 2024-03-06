import discord

class check_role_on_user():
    def __init__(self, required_role_ids: list[int]):
        self.required_role_ids = required_role_ids
    def has_at_least_one_required_role(required_role_ids):
        async def predicate(interaction: discord.Interaction):
            for role_id in required_role_ids:
                if role_id in [role.id for role in interaction.user.roles]:
                    return True
            await interaction.response.send_message("У вас недостаточно прав для использования этой команды.", ephemeral=True)
            return False
        return discord.app_commands.checks.check(predicate)
    
    
    

# def has_at_least_one_required_role(required_role_ids):
#     async def predicate(interaction: discord.Interaction):
#         for role_id in required_role_ids:
#             if role_id in [role.id for role in interaction.user.roles]:
#                 return True
#         await interaction.response.send_message("У вас недостаточно прав для использования этой команды.", ephemeral=True)
#         return False
#     return discord.app_commands.checks.check(predicate)


# def has_required_role_and_send_error(required_role_id):
#     async def predicate(interaction: discord.Interaction):
#         if required_role_id not in [role.id for role in interaction.user.roles]:
#             await interaction.response.send_message("У вас недостаточно прав для использования этой команды.", ephemeral=True)
#             return False
#         return True
#     return discord.app_commands.checks.check(predicate)