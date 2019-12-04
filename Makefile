docker_service_name = api

build:
	docker-compose build $(docker-service-name)

run:
	docker-compose up -d

stop:
	docker-compose stop

logs:
	docker-compose logs --tail=500 --follow $(docker_service_name)

test:
	docker-compose exec $(docker_service_name) python manage.py test chat

make-migrations:
	docker-compose exec $(docker_service_name) python manage.py makemigrations

migrate:
	docker-compose exec $(docker_service_name) python manage.py migrate

django-shell:
	docker-compose exec $(docker_service_name) python manage.py shell

shell:
	docker-compose exec $(docker_service_name) sh

