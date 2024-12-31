# consumer/Dockerfile
FROM python:3.11

# Копируем wait-for-it.sh из родительской директории
COPY wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Копируем ваш код
COPY . /app
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Запускаем wait-for-it перед вашим приложением
CMD ["wait-for-it", "kafka:9093", "--timeout=30", "--", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]