makemigration:
    alembic revision --autogenerate

# start: uvicorn main:app --reload

migrate:
    alembic upgrade head
