install:
	uv sync

migrations:
	uv run python manage.py makemigrations

migrate:
	uv run manage.py migrate

build:
	./build.sh

start:
	uv run manage.py runserver localhost:8000

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check .

test:
	uv run manage.py test

check: test lint

