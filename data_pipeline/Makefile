# Automation of some common operations for local development

all:
	$(error please pick a target)

init-db:
	sqlite3 hikes.db < schema.sql

deploy:
	ak deploy --manifest ./autokitteh.yaml --file pipeline.py

logs:
	ak session log --prints-only
