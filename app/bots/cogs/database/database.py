import os
import mariadb
from io import BytesIO
from PIL import Image

class MariaDBManager:
    def __init__(self, user, password, host, database):
        self.config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database,
        }
        self.connect()

    def connect(self):
        self.db_mariadb = mariadb.connect(**self.config)
        self.cursor = self.db_mariadb.cursor()

    def disconnect(self):
        self.cursor.close()
        self.db_mariadb.close()

    def create_database(self, database_name):
        query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
        self.cursor.execute(query)
        self.db_mariadb.commit()

    def use_database(self, database_name):
        self.config['database'] = database_name
        self.connect()

    def create_table(self, table_name, columns):
        table_structure = ', '.join([f'{column} {columns[column]}' for column in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_structure});"
        self.cursor.execute(query)
        self.db_mariadb.commit()

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(query, tuple(data.values()))
        self.db_mariadb.commit()
        
    def update_data(self, table_name, new_data, condition_column, condition_value):
        """
        Метод для обновления данных в таблице.
        :param table_name: Имя таблицы.
        :param new_data: Словарь с данными для обновления.
        :param condition_column: Название столбца, по которому выполняется условие.
        :param condition_value: Значение условия.
        """
        columns = ', '.join(f"{column} = %s" for column in new_data)
        query = f"UPDATE {table_name} SET {columns} WHERE {condition_column} = %s;"
        values = tuple(new_data.values()) + (condition_value,)
        self.cursor.execute(query, values)
        self.db_mariadb.commit()

    def delete_all_data(self, table_name):
        """
        Метод для удаления всех данных из таблицы.
        :param table_name: Имя таблицы.
        """
        query = f"DELETE FROM {table_name};"
        self.cursor.execute(query)
        self.db_mariadb.commit()

    def get_data_by_condition(self, table_name, condition_column, condition_value):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {condition_column} = %s", (condition_value,))
        return self.cursor.fetchall()

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

            self.db_mariadb.commit()
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
                            self.db_mariadb.commit()
                            print(f"Executed '{filename}' successfully.")

"""

# Пример создания экземпляра класса MariaDBManager
db_manager = MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')

# Пример создания новой базы данных
db_manager.create_database('new_database')

# Пример использования созданной базы данных
db_manager.use_database('new_database')

# Пример создания новой таблицы
columns = {'id': 'INT AUTO_INCREMENT PRIMARY KEY', 'user_id': 'VARCHAR(255)', 'image': 'BLOB', 'text_message': 'TEXT'}
db_manager.create_table('new_table', columns)

# Пример вставки данных
data_to_insert = {'user_id': '123', 'image': b'\x89PNG\r\n\x1a\n...', 'text_message': 'Hello, World!'}
db_manager.insert_data('new_table', data_to_insert)

# Пример получения и обработки данных
user_id_to_process = '123'
db_manager.process_data(user_id_to_process, 'new_table')

# Пример отключения от базы данных
db_manager.disconnect()

# Пример использования запуск sql файлов
db_manager = MariaDBManager(user='root', password='', host='localhost', database='lsc-bot-system-database')
db_manager.execute_sql_file('create_tables.sql')

"""
