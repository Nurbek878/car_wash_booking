generate:
	@echo "Please provide a migration name by running 'make generate NAME=your_migration_name'"

generate-migration:
	alembic revision --message "$(NAME)" --autogenerate

migrate:
	alembic upgrade head

run:
	sudo systemctl stop postgresql
	sudo docker start postgres
	uvicorn app.main:app --reload