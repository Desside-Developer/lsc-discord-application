from ..logging import logs_responde
import logging
print = logging.info

async def get_user_owner():
    data = logs_responde.client.get_user(960251916762378241)
    print(data)