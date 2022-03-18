#-----------------------------------------
# SETTINGS
#-----------------------------------------

POETRY = poetry
RUN = @$(POETRY) run

ifeq ($(ENV), LOCAL)
	PYTHON = @$(RUN) python
else
	PYTHON = python
endif

#-----------------------------------------
# TARGETS
#-----------------------------------------

.PHONY: install dev debug lint autoflake pysenformat pysenlint test

install:
	@$(POETRY) install

dev:
	@$(RUN) uvicorn app.main:app \
			--host 0.0.0.0 \
			--reload

debug:
	sh -c "python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

lint: autoflake pysenformat pysenlint

autoflake:
	@$(RUN) autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables .

pysenformat:
	@$(RUN) pysen run format

pysenlint:
	@$(RUN) pysen run lint

test:
	@$(RUN) pytest
