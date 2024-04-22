from typing import Dict, List, Optional, Tuple, Union

import aiohttp
from aiocache import cached
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing_extensions import TypedDict, Literal



DISCORD_URL = "https://discord.com"
DISCORD_API_URL = f"{DISCORD_URL}/api/v10"
DISCORD_OAUTH_URL = f"{DISCORD_URL}/api/oauth2"
DISCORD_TOKEN_URL = f"{DISCORD_OAUTH_URL}/token"
DISCORD_OAUTH_AUTHENTICATION_URL = f"{DISCORD_OAUTH_URL}/authorize"\

API_ENDPOINT = "https://discord.com/api/v10"

session = aiohttp.ClientSession()

class DiscordClientOAuth:
  client_id: str
  client_secret: str
  redirect_url: str
  session: aiohttp.ClientSession | None

  def __init__(self, client_id, client_secret, redirect_url):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_url = redirect_url

  async def setup(self):
    self.session = aiohttp.ClientSession()

  async def get_user(self, token):
    header = {"Authorization": f"Bearer {token}"}
    async with self.session.get("https://discord.com/api/users/@me", headers=header) as response:
      return await response.json()

  async def get_guilds(self, token):
    header = {"Authorization": f"Bearer {token}"}
    async with self.session.get("https://discord.com/api/users/@me/guilds", headers=header) as response:
      return await response.json()

  async def get_token_response(self, data):
    print('test')
    response = await self.session.post('%s/oauth2/token' % API_ENDPOINT, data=data)
    response.raise_for_status()
    print('test2')
    json_response = await response.json()
    print(json_response)
    
    access_token = json_response.get("access_token")
    refresh_token = json_response.get("refresh_token")
    expires_in = json_response.get("expires_in")
    
    if not access_token or not refresh_token:
        return None
    return access_token, refresh_token, expires_in