# Блок продакшн
build:
	docker-compose -f docker-compose.yml build $(c)
up:
	docker-compose -f docker-compose.yml up -d $(c)
start:
	docker-compose -f docker-compose.yml start $(c)
down:
	docker-compose -f docker-compose.yml down $(c)
destroy:
	docker-compose -f docker-compose.yml down -v $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
run:
	docker-compose -f docker-compose.yml up --build -d

# Блок разработки
run_dev: up_dev upgrade_dev

up_dev:
	docker-compose -f docker-compose.dev.yml up -d --build

upgrade_dev:
	docker-compose -f docker-compose.dev.yml exec auth-dev-app flask db upgrade

api_tests:
	docker-compose -f tests/functional/docker-compose.yml up

db_init_migrate: database_init database_migrate

database_init:
	docker-compose -f docker-compose.dev.yml exec auth-dev-app flask db init

database_migrate:
	docker-compose -f docker-compose.dev.yml exec auth-dev-app flask db migrate

stop_dev:
	docker-compose -f docker-compose.dev.yml stop

destroy_dev:
	docker-compose -f docker-compose.dev.yml down -v $(c)