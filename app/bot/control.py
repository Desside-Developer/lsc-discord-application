import sys
sys.path.append('/code/app/bots')
sys.path.append('/code/app/bots/handlers')
sys.path.append('/code/app/bots/commands')
sys.path.append('/code/app/bots/events')
sys.path.append('/code/app/bots/tickets')

import json

from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query

# from app.bots.logs.manager.save_logs_txt import get_user_owner
from app.bot.database.database import dbMaria
from app.bot import config
from app.bot.main import client_bot

# Routes
from app.bot.database import database
from app.bot.message_system import message
from app.bot.settings import configuration

class FastApi(FastAPI):
    def __init__(self, title_name):
        super().__init__(title=title_name)
    async def on_event(self, event: str):
        print(f"FastAPI event: {event}")
app = FastApi(title_name='[API]: Lsc-Discord-Application')

# Includes Routers
app.include_router(database.router)
app.include_router(message.router)
app.include_router(configuration.router)

@app.post("/api/v1/bot/start")
async def start_bot():
    await client_bot.start(config.Bot_tickets)
    return {"message": "Bot started successfully."}

@app.post("/api/v1/bot/stop")
async def stop_bot():
    await client_bot.close()
    return {"message": "Bot stopped successfully."}

@app.get(path='/bot/ext', description="All Extensions", deprecated=False)
async def all_ext():
    try:
        return client_bot.extensions
    except HTTPException as error:
        print(f'Error: {error}')

@app.get(path='/bot/start-ext', description="Start all Ext", deprecated=False)
async def start_ext():
    for ext in config.cogslist:
        await client_bot.load_extension(ext)

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


@app.get('/test/test', deprecated=False)
async def test_test():
    data = dbMaria.get_all_data('guild_configuration')
    return data
    # for guilds in data:
        # print(guilds)