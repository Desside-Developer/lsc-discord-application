from fastapi import APIRouter, HTTPException, Query
import os
import mysql.connector
from io import BytesIO
from PIL import Image
import config
# from .check import generate_unique_token
# import datetime
# import json

router = APIRouter()
DB_CONFIG = {
    'user': 'root',
    'password': 'pass12345',
    'host': 'db',
    'database': 'lsc-bot-system-database',
}


class MySQLConnectorManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = DB_CONFIG
            cls._instance.connect()
        return cls._instance
    def connect(self):
        self.db_mysql_connector = mysql.connector.connect(**self.config)
        self.cursor = self.db_mysql_connector.cursor()

    def reconnect(self):
        self.db_mysql_connector.reconnect()
        self.cursor = self.db_mysql_connector.cursor()

    def disconnect(self):
        self.cursor.close()
        self.db_mysql_connector.close()

    def create_database(self, database_name):
        query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
        self.cursor.execute(query)
        self.db_mysql_connector.commit()

    def use_database(self, database_name):
        self.config['database'] = database_name
        self.connect()

    def create_table(self, table_name, columns):
        table_structure = ', '.join([f'{column} {columns[column]}' for column in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_structure});"
        self.cursor.execute(query)
        self.db_mysql_connector.commit()
# -----------------------------------------------------------

# -----------------------------------------------------------
    def insert_data(self, table_name, data):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query, tuple(data.values()))
        self.db_mysql_connector.commit()

    def insert_user_data(self, user_id, unique_id, username, balance, on_joined, inventory):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        query = "INSERT INTO users (user_id, unique_id, username, balance, on_joined, inventory) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (user_id, unique_id, username, balance, on_joined, inventory))
        self.db_mysql_connector.commit()

    def insert_user_tags(self, user_id, name_second, data_register):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        query = f"INSERT INTO tags_users (user_id, name_second, data_register) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (user_id, name_second, data_register))
        self.db_mysql_connector.commit()
        return self.cursor.lastrowid

    def insert_tickets_data(self, ticket_id, user_id, status, channel_id, message_id, created_at, closed_at=None):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        query = f"INSERT INTO tickets (ticket_id, user_id, status, channel_id, message_id, created_at, closed_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (ticket_id, user_id, status, channel_id, message_id, created_at, closed_at))
        self.db_mysql_connector.commit()
        return self.cursor.lastrowid

    def insert_assignment(self, assignment_id, ticket_id, user_id, assigned_at):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        query = f"INSERT INTO assigned_tickets (assignment_id, ticket_id, user_id, assigned_at) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (assignment_id, ticket_id, user_id, assigned_at))
        self.db_mysql_connector.commit()
        return self.cursor.lastrowid
# -----------------------------------------------------------

# -----------------------------------------------------------
    def update_data(self, table_name, new_data, condition_column, condition_value):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        columns = ', '.join(f"{column} = %s" for column in new_data)
        query = f"UPDATE {table_name} SET {columns} WHERE {condition_column} = %s;"
        values = tuple(new_data.values()) + (condition_value,)
        self.cursor.execute(query, values)
        self.db_mysql_connector.commit()

    def delete_all_data(self, table_name):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        query = f"DELETE FROM {table_name};"
        self.cursor.execute(query)
        self.db_mysql_connector.commit()

    def delete_one_data(self, table_name, condition_column, condition_value):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        query = f"DELETE FROM {table_name} WHERE {condition_column} = %s;"
        self.cursor.execute(query, (condition_value,))
        self.db_mysql_connector.commit()

    def get_all_data(self, table_name):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        return results

    def get_data_by_condition(self, table_name, condition_column, condition_value):
        if not self.db_mysql_connector.is_connected():
            self.reconnect()
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {condition_column} = %s", (condition_value,))
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        return results

    def get_data_by_user_id(self, user_id, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def process_data(self, user_id, table_name):
        results = self.get_data_by_user_id(user_id, table_name)

        for row in results:
            user_id, image_data, text_message = row
            if image_data:
                image = Image.open(BytesIO(image_data))
                image.save(f"user_{user_id}_image.jpg")

            if text_message:
                print(f"User {user_id} sent a text message: {text_message}")

    def execute_sql_file_in_subfolder(self, subfolder, filename):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        sql_file_path = os.path.join(current_directory, subfolder, filename)
        if os.path.exists(sql_file_path):
            with open(sql_file_path, 'r') as file:
                queries = file.read().split(';')

            for query in queries:
                query = query.strip()
                if query:
                    self.cursor.execute(query)

            self.db_mysql_connector.commit()
        else:
            print(f"File '{filename}' not found in subfolder '{subfolder}'.")

    def execute_all_sql_files_in_subfolder(self, subfolder):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        sql_files_path = os.path.join(current_directory, subfolder)
        for filename in os.listdir(sql_files_path):
            if filename.endswith('.sql'):
                table_name = os.path.splitext(filename)[0]
                with open(os.path.join(sql_files_path, filename), 'r', encoding='utf-8') as file:
                    queries = file.read().split(';')
                    for query in queries:
                        query = query.strip()
                        if query:
                            try:
                                self.cursor.execute(query)
                                self.db_mysql_connector.commit()
                                print(f"Executed '{table_name}' successfully.")
                            except mysql.connector.Error as err:
                                if err.errno == 1050: 
                                    print(f"Table '{table_name}' already exists, skipping.")
                                elif err.errno == 1005:
                                    print(f"Error creating table '{table_name}': {err}")
                                else:
                                    print(f"An unexpected error occurred: {err}")

    def execute_sql_files(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.abspath(os.path.join(current_directory, '..'))
        sql_files_path = os.path.join(parent_directory, 'entities')
        for files in config.files_order:
            file_path = os.path.join(sql_files_path, files)
            if os.path.isfile(file_path) and files.endswith('.sql'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                queries = [query.strip() for query in content.split(';') if query.strip()]
                for query in queries:
                    try:
                        self.cursor.execute(query)
                        self.db_mysql_connector.commit()
                        print(f"Executed query successfully: {query}")
                    except Exception as e:
                        print(f"Error executing query in {files}: {str(e)}")
                        print(f"Problematic query: {query}")

    def execute_all_sql_files_in_sql_dates(self, subfolder: str, subsql: str):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        sql_files_path = os.path.join(current_directory, subfolder)

        for filename in os.listdir(sql_files_path):
            file_path = os.path.join(sql_files_path, filename)

            if os.path.isfile(file_path) and filename.endswith('.sql'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                if content.startswith(subsql):
                    print(f"Processing file: {filename}")

                    queries = [query.strip() for query in content.split(';') if query.strip()]
                    for query in queries:
                        try:
                            self.cursor.execute(query)
                            self.db_mysql_connector.commit()
                            print(f"Executed query successfully: {query}")
                        except Exception as e:
                            print(f"Error executing query in {filename}: {str(e)}")
                            print(f"Problematic query: {query}")

                    print(f"Execution successful for file: {filename}")
                else:
                    print(f"File '{filename}' does not start with '{subsql}'")
            else:
                print(f"Error: '{filename}' is not a valid SQL file")


dbMaria = MySQLConnectorManager()

router.tags = ["Database ('LSC-BOT')"]

@router.get(path='/database/insert/user_data', description="Insert Data From Users")
async def insert_user_data(user_id: str = Query("14523513251", description=f"User_id")):
    dbMaria.insert_user_data(user_id=user_id,unique_id="dat",username="dat",balance="dat",on_joined="dat",inventory="dat")