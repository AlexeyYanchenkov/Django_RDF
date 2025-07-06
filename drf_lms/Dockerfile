# 1. Используем официальный базовый образ Python 3.10.12 на базе slim (уменьшенный размер)
FROM python:3.10.12-slim

# 2. Отключаем создание .pyc-файлов и буферизацию вывода (удобно для логов)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Указываем рабочую директорию внутри контейнера
WORKDIR /code

# 4. Копируем только файл зависимостей на этом этапе
# Это позволяет использовать кэш, если requirements.txt не изменился
COPY requirements.txt /code/

# 5. Обновляем pip и устанавливаем зависимости проекта
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --verbose

# 6. Копируем весь проект в контейнер (в текущую директорию WORKDIR /code)
COPY . /code/

# 7. Указываем команду по умолчанию — запуск в режиме разработки
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]