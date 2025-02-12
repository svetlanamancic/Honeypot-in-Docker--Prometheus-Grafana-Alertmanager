THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: up stop ps logs
up:
	docker compose -f docker-compose.yml up --build -d $(c)
stop:
	docker compose -f docker-compose.yml stop $(c) 
ps:
	docker compose -f docker-compose.yml ps 
logs:
	docker compose -f docker-compose.yml logs --tail=100 -f $(c)


