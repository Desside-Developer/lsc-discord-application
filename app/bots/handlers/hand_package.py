import datetime
import json

from .generate.unique_token import generate_unique_token
from database.database import dbMaria

async def check_user(id, user_name):
    """
    Данная функция создана для проверки того что пользователь есть в таблице главной users.
    - Функция принимает
    -- id ( Айди пользователя )
    -- user_name ( Имя пользователя )
    """
    user = dbMaria.get_data_by_condition('users', condition_column='user_id',condition_value=id)
    if user == []:
        user_id = id
        unique_id = generate_unique_token()
        username = user_name
        balance = 0
        on_joined = datetime.datetime.now()
        inventory = {}
        dbMaria.insert_user_data(user_id, unique_id, username, balance, on_joined, json.dumps(inventory))
        return True
    else:
        return False

async def get_user_by_id(id):
    user = dbMaria.get_data_by_condition('users', condition_column='user_id', condition_value=id)
    return user[0]

async def save_user_to_database(id):
    dbMaria.insert_data('users', user_id=id)

async def check_user_tags(id):
    user = dbMaria.get_data_by_condition('tags_users', condition_column='user_id', condition_value=id)
    if user == []:
        return False
    else:
        return True

async def save_user_tags(id, name_second):
    user_id = id
    data_register = datetime.datetime.now()
    dbMaria.insert_user_tags(user_id, name_second, data_register)
    return await get_user_by_id(id)