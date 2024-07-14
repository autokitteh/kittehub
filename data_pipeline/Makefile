# Automation of some common operations for local development

all:
	$(error please pick a target)

init-db:
	sqlite3 hikes.db < schema.sql

deploy:
	ak deploy --manifest ./autokitteh.yaml --file pipeline.py

vars:
	ak var set --env pipeline/default DB_DSN $(PWD)/hikes.db
	ak var set --secret --env pipeline/default AWS_ACCESS_KEY_ID $(AWS_ACCESS_KEY_ID)
	ak var set --secret --env pipeline/default AWS_SECRET_KEY $(AWS_SECRET_KEY)

trigger:
	curl -d @example-sns-event.json http://localhost:9980/http/pipeline/new_object

logs:
	ak session log --prints-only
