FROM python:3.12

WORKDIR /code

COPY bot/ /code/bot/
COPY requirements.txt /code/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["sh", "-c", "python bot/bot.py & uvicorn bot.control:app --host 0.0.0.0 --port 6960 --reload"]
