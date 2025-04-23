install:
	uv sync

build:
	./build.sh

start:
	uv run manage.py runserver localhost:8010

render-start:
	gunicorn task_manager.wsgi

check:
	uv run ruff check .

check-fix:
	uv run ruff check --fix .

test:
	uv run manage.py test

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

migrations-user:
	python manage.py makemigrations user

collectstatic:
	python manage.py collectstatic --no-input

translate-compile:
	django-admin compilemessages

translate-makemessages:
	django-admin makemessages -l ru

tests:
	python manage.py test

tests-cov:
	uv run coverage run ./manage.py test
	uv run coverage xml

