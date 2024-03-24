from pydantic import BaseModel, Field
from fastapi import FastAPI, Query
from app.bots.database.database import dbMaria
from api.routes import database
import json

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