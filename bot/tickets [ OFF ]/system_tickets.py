from .. import *
# print(settingsTicketSystem['name'])


class system(cm.Cog):
  NameCog = "SystemTickets"
  def __init__(self, client:cm.Cog):
    self.client = client

async def setup(client: cm.Bot) -> None:
  try:
    await client.add_cog(system(client))
    raise HTTPException(200, f": Cog {system.NameCog} added.")
    # print(f"Ok: Cog '{SystemTickets.__name__}' successfully added.")
  except Exception as error:
    raise(404, f"Exception: Error adding cog >>> {system.NameCog} >>> {error}")
    # print(f"Exception: Error adding cog >>> '{SystemTickets.__name__}': {error}")