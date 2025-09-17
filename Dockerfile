FROM python:3.10-slim

RUN apt update && apt install -y liblzo2-dev && apt clean

# Устанавливаем poetry
RUN pip install poetry==1.3.2

# Убедим Poetry не страдать фигнёй
RUN poetry config virtualenvs.create false

# Копируем зависимости сначала — для кеша
COPY ./poetry.lock ./pyproject.toml /usr/src/app/
WORKDIR /usr/src/app/

# Установка зависимостей
RUN poetry install --no-root --no-interaction

# Копируем весь проект
COPY . /usr/src/app/

# Запуск
CMD ["python", "backend.py"]
