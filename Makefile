start:
	uvicorn main:app --reload

makemigration:
	alembic revision --autogenerat

migrate:
	alembic upgrade head
