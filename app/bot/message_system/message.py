import discord
from discord import HTTPException as DiscordHTTP
from discord.ext import commands
from fastapi import APIRouter, HTTPException
# class messages_system(commands.Bot):
    # def __init__(self, client: commands.Bot):
        # self.client = client

router = APIRouter()

message_system = "Message System ('Bot_Discord')"
router.tags = [message_system]


# ['content', 'color', 'description', 'attachments']
data = {
    "content": "@Everyone",
    "embeds": [
        {
            "content": "This Embed",
            "color": "0xffffff",
            "description": "this data for new data",
            "attachments": {
                "set_author": {
                "content": "Hello im Author!",
                "name": "Dan",
                "url": "http://localhost:5345",
                "icon_url": "http://localhost:5345",
                },
                "set_footer": {
                "content": "Im Footer",
                "icon_url": "http://localhost/url/img",
                },
                "set_image": {
                "url": "http://localhost/url/img",
                },
                "set_thumbnail": {
                "url": "http://localhost/url/img",
                },
                "add_field": {
                "content": "Im new fIELD",
                "name": "mY nAME",
                "value": None,
                "inline": True,
                },
                "set_field_at": {
                "index": 1,
                "name": "hee",
                "value": None,
                "inline": False,
                }
            }
        }
    ]
}

async def data_f(data) -> None:
    if data['content'] == str:
        return print('Error1')
    if data['embeds'] == list:
        return print('Error')
    elements = [item for item in data['embeds']]; elements=elements[0]
    if elements != dict:
        data_list=['content','color','description','attachments']
        for items in data_list:
            if type(elements[items]) == str:
                print(f'Type : {type(elements[items])} == STR')
            if type(elements[items]) == dict:
                data_item = elements[items]
                for items in data_item:
                    if type(data_item[items]) == dict:
                        colums={
                            "set_author": {
                                "content": str,
                                "name": str,
                                "url": str,
                                "icon_url": str
                                },
                            'set_footer': {
                                "content": str,
                                "icon_url": str
                                },
                            'set_image': {
                                "url": str
                                },
                            'set_thumbnail': {
                                "url": str
                                },
                            'add_field': {
                                "content": str,
                                "name": str,
                                "value": int,
                                "inline": bool
                                },
                            'set_field_at': {
                                "index": int,
                                "name": str,
                                "value": int,
                                "inline": bool
                            }
                        }
                        data_items = data_item[items]
                        for column in colums[items]:
                            if column in data_item[items]:
                                if colums[items][column] == type(data_item[items][column]):
                                    print(f"Data : {colums[items][column]} > {type(data_item[items][column])}")
                            else:
                                return print('not ok 3')
                    else:
                        return print('not ok 4')
        return await creating_embed(..., data=data)

async def creating_embed(ctx: commands.Context, data:dict):
    # emb = discord.Embed(title=)
    print('test')
    print(data['content'])

@router.get(path='/start/function/data_f', deprecated=False)
async def start_this():
    await data_f(data)

# async def setup(client:commands.Bot) -> None:
#     try:
#         await client.add_cog(messages_system(client))
#         print('System Message Load ?')
#     except HTTPException as error:
#         print(f"Error: {error}")