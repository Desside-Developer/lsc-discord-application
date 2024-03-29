from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, Query
import redis
from app.bots.database.database import dbMaria
from api.routes import database
import json
from app.bots.logs.manager.save_logs_txt import get_user_owner

class FastApi(FastAPI):
    def __init__(self, title_name):
        super().__init__(title=title_name)
    async def on_event(self, event: str):
        print(f"FastAPI event: {event}")

app = FastApi(title_name="[API] TestSystem")
app.include_router(database.router)

@app.get('/discord/bot/sql-execute-subfolder', tags=["database-discord-bot"], description="Execute all sql files on subfolder")
async def read_root(subfolder:str = Query(..., description=f"test")):
    try:
        dbMaria.execute_all_sql_files_in_subfolder(subfolder=subfolder)
    except Exception as e:
        print(f'Error: {e}')

@app.post('/discord/bot/sql-execute-subfolder-sql', tags=["database-dicsord-bot"], description="Execute sql file on subfolder")
async def read_root(subfolder: str, subsql: str):
    try:
        dbMaria.execute_all_sql_files_in_sql_dates(subfolder=subfolder, subsql=subsql)
    except Exception as e:
        print(f"Error: {e}")
@app.get('/discord/bot/sql-fl-sq', tags=["database-discord-bot"], description="test")
async def read_root_sub_fl_sq(subfolder:str = Query(..., description=f"test"), subsql:str = Query(..., description=f"test")):
    try:
        dbMaria.execute_all_sql_files_in_sql_dates(subfolder=subfolder, subsql=subsql)
    except Exception as e:
        print(f'Error: {e}')
@app.get('/discord/bot/test', tags=["none"], description="test")
async def read_root():
    data = dbMaria.get_data_by_condition('tickets', 'ticket_id', 'LNVTC58QYN'); data = data[0]
    return int(data['channel_id'])
@app.get('/test', description="rr")
async def test():  
    await get_user_owner()
    print('ready')

redis_host = 'bot-redis-stack-1'
redis_port = 6379
redis_db = 0
r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
# SET
@app.get('/redis/set/{key}/{value}', description="Set a value in Redis")
async def set_value(key: str, value: str):
    try:
        r.set(key, value)
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail="Error communicating with Redis") from e
    return {"message": f"Key '{key}' set to value '{value}' in Redis"}

# GET
@app.get('/redis/get/{key}', description="Get a value from Redis")
async def get_value(key: str):
    try:
        value = r.get(key)
        value_str = value.decode() if value else "Key not found"
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail="Error communicating with Redis") from e
    return {"message": f"Value for key '{key}' in Redis: {value_str}"}

# DELETE
@app.delete('/redis/delete/{key}', description="Delete a key from Redis")
async def delete_key(key: str):
    try:
        deleted_count = r.delete(key)
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail="Error communicating with Redis") from e
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Key '{key}' not found in Redis")
    else:
        return {"message": f"Key '{key}' deleted from Redis"}

# KEYS
@app.get('/redis/keys/{pattern}', description="Find keys in Redis matching a pattern")
async def find_keys(pattern: str):
    try:
        keys = r.keys(pattern)
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail="Error communicating with Redis") from e
    return {"keys": keys}

# INCR
@app.get('/redis/incr/{key}', description="Increment the value of a key in Redis")
async def increment_key(key: str):
    try:
        new_value = r.incr(key)
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail="Error communicating with Redis") from e
    return {"message": f"Key '{key}' incremented to value '{new_value}' in Redis"}

# EXPIRE
@app.get('/redis/expire/{key}/{seconds}', description="Set a timeout on a key in Redis")
async def set_timeout(key: str, seconds: int):
    try:
        r.expire(key, seconds)
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail="Error communicating with Redis") from e
    return {"message": f"Key '{key}' set to expire in {seconds} seconds"}

# PING
@app.get('/redis/ping', description="Ping Redis server")
async def ping_redis():
    try:
        response = r.ping()
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail="Error communicating with Redis") from e
    
    if response:
        return {"message": "Redis server is reachable"}
    else:
        raise HTTPException(status_code=500, detail="Failed to ping Redis server")

# Additional commands can be added as needed