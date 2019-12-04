docker_service_name = api

build:
	docker-compose build $(docker-service-name)

run:
	docker-compose up -d

stop:
	docker-compose stop

logs:
	docker-compose logs --tail=500 --follow $(docker-service-name)

test:
	docker-compose exec $(docker-service-name) python manage.py test chat
