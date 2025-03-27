FROM python:3.11-slim

WORKDIR /gena_server

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Запускаем миграции и сервер
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
