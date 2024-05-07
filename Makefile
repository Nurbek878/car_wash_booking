generate:
	alembic revision --m=$(NAME) --autogenerate

migrate:
	alembic upgrade head

run:
	uvicorn app.main:app --reload