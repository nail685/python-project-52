install:
	uv sync

migrate:
	uv run manage.py migrate

migrations:
	uv run python manage.py makemigrations

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

