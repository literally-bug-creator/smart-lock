NW = $(wordlist 2, 2, $(MAKECMDGOALS))


build:
	@docker compose build


run:
	@if [ -n "$(NW)" ]; then \
		docker compose up -d --scale celery_worker=$(NW); \
	else \
		docker compose up -d; \
	fi


stop:
	@docker compose stop


down:
	@docker compose down


restart:
	@docker compose restart


%:
	@:
