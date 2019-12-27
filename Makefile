service_name = api

build:
	docker-compose build $(service_name)

run:
	docker-compose up -d

stop:
	docker-compose stop

restart:
	docker-compose restart

logs:
	docker-compose logs --tail=500 --follow $(service_name)

test:
	docker-compose exec $(service_name) python manage.py test chat

make-migrations:
	docker-compose exec $(service_name) python manage.py makemigrations

migrate:
	docker-compose exec $(service_name) python manage.py migrate

django-shell:
	docker-compose exec $(service_name) python manage.py shell

bash:
	docker-compose exec $(service_name) /bin/bash

