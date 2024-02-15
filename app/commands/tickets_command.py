from app.bots.bot_tickets import tree


@tree.command(name='ticket', help='Create a ticket')
async def ticket_command(ctx):
    # Твой код для создания тикета здесь
    await ctx.send('Ticket created!')


@tree.slash_command(name='ticket', description='Create a ticket')
async def slash_ticket_command(ctx):
    # Твой код для создания тикета здесь
    await ctx.send('Ticket created!')
