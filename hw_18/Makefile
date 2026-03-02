.PHONY: dev.install db.migration.new db.migrate db.rollback

dev.install:
	pip install -r requirements.txt

db.migration.new:
	yoyo new ./migrations -m "$(name)"

db.migrate:
	yoyo apply --database "$$(python -c 'from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv("DATABASE_URL"))')" ./migrations

db.rollback:
	yoyo rollback --database "$$(python -c 'from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv("DATABASE_URL"))')" ./migrations
