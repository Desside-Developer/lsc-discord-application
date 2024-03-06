from database import MariaDBManager

# Создание экземпляра класса MariaDBManager
db_manager = MariaDBManager(user='root', password='', host='db', database='lsc-bot-system-database')

# Создание таблицы (вызывайте только при первом запуске)
db_manager.create_table()

# Пример сохранения данных
db_manager.save_image_and_text(user_id='YYY', image_path='path/to/your/image.jpg', text_message='Привет, как дела?')

# Пример получения и обработки данных
db_manager.process_data(user_id='YYY')

# Отключение от базы данных
db_manager.disconnect()