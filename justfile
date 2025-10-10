#!/usr/bin/env just --justfile

# Run this the first time to set up the project
# Make sure you have a PostgreSQL database running in docker with a user 'postgres' and password 'postgres
dev-init:
	docker exec -i postgres psql -U postgres -c "create database weg_solutions;"

install-uv:
	pip install uv

requirements: install-uv
	uv pip compile requirements.in -o requirements.txt
	uv pip sync requirements.txt

	uv pip compile dev-requirements.in -o dev-requirements.txt
	uv pip sync dev-requirements.txt

update-css:
    npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css

watch-css:
    npm run dev-watch

runserver:
	python manage.py runserver

shell:
	python manage.py shell

upgrade_user email:
	python manage.py promote_user_to_superuser {{email}}


celery:
	watchfiles --filter python 'celery -A weg_solutions worker --loglevel=INFO'

