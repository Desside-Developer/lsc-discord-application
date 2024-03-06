from pypresence import Presence
import time
from datetime import datetime
import pytz  # Для работы с часовыми поясами

# Задаем дату и время начала в формате "год-месяц-день часы:минуты:секунды"
start_time_str = "2023-01-01 12:00:00"
# Преобразуем строку в объект datetime в UTC
start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
start_time = start_time.replace(tzinfo=pytz.UTC)

# Преобразуем объект datetime в секунды с начала эпохи
start_seconds = int(time.mktime(start_time.timetuple()))

client_id = "1211445052912705626"  # Id from the application developer portal

RPC = Presence(client_id)
RPC.connect()

# Обновите эту часть, чтобы она отражала реальные данные и ключи изображений из вашего Discord Developer Portal
RPC.update(
    state=f"Do you love dogs?!",
    details="Im beginner!",
    start=start_seconds,  # Используем вычисленное время начала
    large_image="https://w.forfun.com/fetch/c6/c6698083dd716a8f0676763322640926.jpeg",  # Ключ большого изображения, загруженного в ваше приложение Discord
    large_text="Пёсик ;)",
    small_image="https://discords.com/_next/image?url=https:%2F%2Fcdn.discordapp.com%2Femojis%2F796395392202834000.gif&w=48&q=75",  # Ключ маленького изображения, загруженного в ваше приложение Discord
    small_text="Галочка",
    buttons=[{"label": "Start", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},  # URL для перехода по клику на кнопку
             {"label": "Check Profile", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}]  # Можно добавить до 2 кнопок
)

while True:
    time.sleep(15)  # Задержка для снижения нагрузки на цикл
