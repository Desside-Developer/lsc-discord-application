from .__init__ import *

import subprocess
import asyncio
import uuid
from typing import List, Literal, TypedDict
# Settigs Imports
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query, Depends, Request, Response, Cookie
from fastapi.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth
from fastapi.responses import RedirectResponse

from .config import BOT_APPLICATION_ID, BOT_CLIENT_SECRET, BOT_REDIRECT_URL

from starlette.templating import Jinja2Templates

from .authentication import client

from discord.ext.ipc import Client as ClientIpc

from .handlers import interactions

# from .routes.authentication import DiscordOAuthClient, RateLimited, Unauthorized, User
# from .routes.authentication.exceptions import ClientSessionNotInitialized
# from .routes.authentication.models import GuildPreview

# from routes.authentication
# Import Database:
# None

# Routes Imports
# from app.bot.database import database
# from app.bot.message_system import message
# from app.bot.settings import configuration

class FastApi(FastAPI):
    def __init__(self, title_name):
        super().__init__(title=title_name)
    async def on_event(self, event: str):
        print(f"FastAPI event: {event}")
app = FastApi(title_name='[API]: LSC-SANTOS-CASTOM-DISCORD-APPLICATION')
templates = Jinja2Templates(directory="/code/bot/frontend")
discordApi = client.DiscordClientOAuth(client_id=BOT_APPLICATION_ID, client_secret=BOT_CLIENT_SECRET, redirect_url=BOT_REDIRECT_URL)
# discord = DiscordOAuthClient(
#     "1190823471886893256", "um69RKeC8rUxxUi0aOwERB6yYd8LjVPZ", "http://localhost:4547/callback", ("identify", "guilds", "email")
# )  # scopes

async def startup():
  await discordApi.setup()

def on_startup():
  asyncio.create_task(startup())
on_startup()


# Tags Api
webserver = '[Web-Server]'
api_base = '[Api-Standart]'
tag_auth = '[Authentification-Discord]'

# End-Points Settings
url_api = 'api'

# Includes Routers
# app.include_router()
app.include_router(interactions.router)

# app.add_event_handler("startup", on_startup)
# import docker
# def get_container_ip(container_name):
    # client = docker.from_env()
    # try:
        # container = client.containers.get(container_name)
        # ip_address = container.attrs['NetworkSettings']['Networks']['my_network']['IPAddress']
        # return ip_address
    # except docker.errors.NotFound:
        # print(f"Container {container_name} not found")
        # return None
    # except Exception as e:
        # print(f"Error occurred while getting IP address for container {container_name}: {e}")
        # return None

# Пример использования
# server_container_name = "server"
# server_ip_address = get_container_ip(server_container_name)
# if server_ip_address:
#     print(f"IP address of server container: {server_ip_address}")
# else:
#     print("Failed to get IP address of server container")

# Подключаемся к серверу IPC, используя IP-адрес
# if server_ip_address:
#   print(server_ip_address)
appDiscord = ClientIpc(host="bot",secret_key="test01")
  # Используйте IP-адрес вместо имени контейнера при создании клиента IPC

@app.get('/test/get')
async def test01():
  user = await appDiscord.request("get_user_data", user_id=960251916762378241)
  return user.response 



@app.get('/')
async def home(request: Request):
  guild_count = await appDiscord.request("get_guilds")
  return templates.TemplateResponse(
    "index.html",
    {
      "request": request,
      "count": guild_count.response,
      "login_url": "https://discord.com/oauth2/authorize?client_id=1190823471886893256&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A4547%2Fcallback&scope=gdm.join+guilds+identify"
    }
  )

class TokenGrantPayload(TypedDict):
    client_id: str
    client_secret: str
    grant_type: Literal["authorization_code"]
    code: str
    redirect_uri: str

# @app.get("/login")
# async def login():
#   return {"url": "https://discord.com/oauth2/authorize?client_id=1190823471886893256&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A4547%2Fcallback&scope=identify+guilds+gdm.join"}

@app.get("/callback")
async def callback(code: str):
  data = {
    'client_id':BOT_APPLICATION_ID,
    'client_secret':BOT_CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': BOT_REDIRECT_URL
  }
  result = await discordApi.get_token_response(data=data)
  if result is None:
    raise HTTPException(status_code=401, detail="Invalid Auth Code")
  
  token, refresh_token, expires_in = result
  user = await discordApi.get_user(token)
  user_id = user.get("id")
  session_id= str(uuid.uuid4())
  interactions.dbMaria.insert_sessions(session_id, token, refresh_token, expires_in, user_id)
  print(session_id)
  response = RedirectResponse(url="/guilds")
  response.set_cookie(key="session_id", value=session_id, httponly=True)
  return response
  # return {"access_token": token, "refresh_token": refresh_token}


@app.get("/authenticated")
async def isAuthenticated(token):
  try:
    return True
  except Exception as e:
    return False


# @app.exception_handler()
# async def unauthorized_error_handler(_, __):
    # return JSONResponse({"error": "Unauthorized"}, status_code=401)


# @app.exception_handler()
# async def rate_limit_error_handler():
    # return JSONResponse()


# @app.exception_handler()
# async def client_session_error_handler():
    # return JSONResponse({"error": "Internal Error"}, status_code=500)


@app.get("/user")
async def get_user(user):
    return user


@app.get("/guilds")
async def get_guilds(request: Request):
  session_id = request.cookies.get("session_id")
  print(session_id)
  if not session_id:
    raise HTTPException(status_code=401, detail="no auth")
  session = interactions.dbMaria.get_sessions(session_id)
  
  user = await discordApi.get_user(session["token"])
  user_guilds = await discordApi.get_guilds(session["token"])
  
  return user_guilds

# Эндпоинт для перенаправления на страницу авторизации Discord
# discord_client = oauth.create_client('discord')
# @app.get(f'/{url_api}/login', tags=[webserver, tag_auth])
# async def api_login():
#     redirect_uri = 'https://discord.com/oauth2/authorize?client_id=1190823471886893256&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A4547%2Fapi%2Fauth%2Fredirect&scope=identify+email+guilds'
#     return await discord_client.authorize_redirect(redirect_uri)

# # Обработка редиректа после авторизации Discord
# @app.get(f'/{url_api}/redirect', tags=[webserver, tag_auth])
# async def api_redirect(request: Request, response: Response, code: str = None, state: str = None):
#     token = await oauth.discord.authorize_access_token(request)
#     # Сохраните токен в куки
#     response.set_cookie(key="token", value=token["access_token"])
#     return RedirectResponse(url='/dashboard')

# # Проверка статуса сеанса
# @app.get(f'/{url_api}/status', tags=[webserver, tag_auth])
# async def api_status(token: str = Cookie(None)):
#     # Проверьте, авторизован ли пользователь
#     if token:
#         # Верните информацию о пользователе, если он авторизован
#         return {'status': 'authorized', 'token': token}
#     else:
#         # Верните ошибку, если нет
#         raise HTTPException(status_code=401, detail="Unauthorized")

# # Выход
# @app.post(f'/{url_api}/logout', tags=[webserver, tag_auth])
# async def api_logout(response: Response):
#     # Удалите токен из куки
#     response.delete_cookie(key="token")
#     return RedirectResponse(url='/')

# @app.get("/dashboard", tags=[webserver])
# async def dashboard(token: str = Cookie(None)):
#     if token:
#         return {"message": "Welcome to the dashboard!"}
#     else:
#         raise HTTPException(status_code=401, detail="Unauthorized")



@app.get('/api/settings')
async def settings_app() -> None:
  raise NotImplementedError('No have idea for this settings')

@app.post('/api/bot/settings/status')
async def settingsApplicationStatus() -> None:
  return client_bot.change_presence(status=discord.Status.do_not_disturb)
  # raise NotImplementedError('No have idea for this settings')

@app.get('/api/bot/settings/test')
async def settingsApplicationTest():
  raise NotImplementedError('No have idea for this settings')