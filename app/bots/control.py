import json
import redis

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query

from app.bots.logs.manager.save_logs_txt import get_user_owner
from app.bots.database.database import dbMaria
from app.bots.database import database
from app.bots.main import client_bot

class FastApi(FastAPI):
    def __init__(self, title_name):
        super().__init__(title=title_name)
    async def on_event(self, event: str):
        print(f"FastAPI event: {event}")
app = FastApi(title_name='[API]: Lsc-Discord-Application')

# Includes Routers
app.include_router(database.router)

@app.get(path='/bot/start', description="This command start bot!", deprecated=True, response_description="Bot Starting!")
async def bot_start():
    pass

@app.get(path='/bot/stop', description="This command stop bot!", deprecated=True, response_description="Bot Stopped!")
async def bot_stop():
    pass

@app.get(path='/bot/ext', description="All Extensions", deprecated=False)
async def all_ext():
    try:
        return client_bot.extensions
    except HTTPException as error:
        print(f'Error: {error}')


@app.post(path='/bot/load-ext', description="Load Extension!", deprecated=False)
async def load_ext(ext: str=Query('path.path.cogs.py', description="Path to Extension!")):
    try:
        await client_bot.load_extension(ext)
    except HTTPException as error:
        print(f'Error: {error}')


@app.post(path='/bot/unload-ext', description="Unload Extension!", deprecated=False)
async def unload_ext(ext: str=Query('path.path.cogs.py', description="Path to Extension!")):
    try:
        await client_bot.unload_extension(ext)
    except HTTPException as error:
        print(f'Error: {error}')


@app.post(path='/bot/reload-ext', description="Reload Extension!", deprecated=False)
async def reload_ext(ext: str=Query()):
    try:
        await client_bot.reload_extension(ext)
    except HTTPException as error:
        print(f'Error: {error}')