import os
import mysql.connector
from io import BytesIO
from PIL import Image

# from .check import generate_unique_token
# import datetime
# import json

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

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query, tuple(data.values()))
        self.db_mysql_connector.commit()

    def insert_user_data(self, user_id, unique_id, username, balance, on_joined, inventory):
        query = "INSERT INTO users (user_id, unique_id, username, balance, on_joined, inventory) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (user_id, unique_id, username, balance, on_joined, inventory))
        self.db_mysql_connector.commit()

    def insert_user_tags(self, user_id, name_second, data_register):
        query = f"INSERT INTO tags_users (user_id, name_second, data_register) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (user_id, name_second, data_register))
        self.db_mysql_connector.commit()
        return self.cursor.lastrowid

    def update_data(self, table_name, new_data, condition_column, condition_value):
        columns = ', '.join(f"{column} = %s" for column in new_data)
        query = f"UPDATE {table_name} SET {columns} WHERE {condition_column} = %s;"
        values = tuple(new_data.values()) + (condition_value,)
        self.cursor.execute(query, values)
        self.db_mysql_connector.commit()

    def delete_all_data(self, table_name):
        query = f"DELETE FROM {table_name};"
        self.cursor.execute(query)
        self.db_mysql_connector.commit()

    def get_data_by_condition(self, table_name, condition_column, condition_value):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {condition_column} = %s", (condition_value,))
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]  # Получаем названия столбцов
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
                with open(os.path.join(sql_files_path, filename), 'r', encoding='utf-8') as file:
                    queries = file.read().split(';')
                    for query in queries:
                        query = query.strip()
                        if query:
                            self.cursor.execute(query)
                            self.db_mysql_connector.commit()
                            print(f"Executed '{filename}' successfully.")
    
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
                # with open(os.path.join(sql_files_path, file), 'r', encoding='utf-8') as file:
                    # queries = ""


dbMaria = MySQLConnectorManager()


# async def check_user(id, user_name):
#     user = dbMaria.get_data_by_condition('users', condition_column='user_id',condition_value=id)
#     if user == []:
#         user_id = id
#         unique_id = generate_unique_token()
#         username = user_name
#         balance = 0
#         on_joined = datetime.datetime.now()
#         inventory = {}
#         dbMaria.insert_user_data(user_id, unique_id, username, balance, on_joined, json.dumps(inventory))
#         return True
#     else:
#         return False

# async def get_user_by_id(id):
#     user = dbMaria.get_data_by_condition('users', condition_column='user_id', condition_value=id)
#     return user[0]

# async def save_user_to_database(id):
#     dbMaria.insert_data('users', user_id=id)

# async def check_user_tags(id):
#     user = dbMaria.get_data_by_condition('tags_users', condition_column='user_id', condition_value=id)
#     if user == []:
#         return False
#     else:
#         return True

# async def save_user_tags(id, name_second):
#     user_id = id
#     data_register = datetime.datetime.now()
#     dbMaria.insert_user_tags(user_id, name_second, data_register)
#     return await get_user_by_id(id)