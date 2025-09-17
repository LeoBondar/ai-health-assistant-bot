PROJECT_NAME = ai_support_bot

# Стандартные команды
.PHONY: up down logs

# Поднять контейнер
up:
	docker-compose -p $(PROJECT_NAME) up -d --build

# Остановить и удалить контейнер, сеть и образ
down:
	docker-compose -p $(PROJECT_NAME) down

# Посмотреть логи контейнера
logs:
	docker-compose -p ${PROJECT_NAME} logs -f



