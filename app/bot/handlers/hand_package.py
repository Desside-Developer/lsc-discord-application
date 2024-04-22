import datetime
import json
import logging

print = logging.info

from colorama import Back, Fore, Style
from .generate.unique_token import generate_unique_token, generate_ticket_token
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
    return True

async def save_user_tags(id, name_second):
    user_id = id
    data_register = datetime.datetime.now()
    dbMaria.insert_user_tags(user_id, name_second, data_register)
    return await get_user_by_id(id)

async def check_name_second(name_second):
    user = dbMaria.get_data_by_condition('tags_users', condition_column='name_second', condition_value=name_second)
    if user == []:
        return False
    return True

async def save_ticket_for_table(ticket_id, user_id, status, channel_id, message_id, created_at):
    try:
        dbMaria.insert_tickets_data(ticket_id, user_id, status, channel_id, message_id, created_at)
        print(f"{Fore.RED}{ticket_id} {Fore.YELLOW}created ticket: {Fore.GREEN}{created_at}{Fore.RESET}")
        return True
    except Exception as e:
        print(f"Error saving ticket to database: {e}")
        return False