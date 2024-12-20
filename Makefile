.ONESHELL:
up:
	clear
	docker-compose up --build

cleaned:
	clear
	docker system prune -a -f
	docker-compose up --build