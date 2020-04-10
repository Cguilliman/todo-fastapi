start:
	uvicorn main:app --reload

makemigration:
	alembic revision --autogZenerat

migrate:
	alembic upgrade head
