generate:
	alembic revision --m=$(NAME) --autogenerate

migrate:
	alembic upgrade head

run:
	sudo systemctl stop postgresql
	sudo docker start postgres
	uvicorn app.main:app --reload