FROM python:3.10-alpine3.16

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.3.1 \
  PIP_VERSION=22.1.2

RUN apk add --update build-base
RUN apk add postgresql-dev python3-dev musl-dev
RUN apk add libxml2-dev libxslt-dev
RUN apk add git
RUN apk add bash
RUN pip install --upgrade "pip==$PIP_VERSION" && pip install "poetry==$POETRY_VERSION"

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \ 
&& poetry install --no-interaction --no-ansi

CMD ["python3", "main.py"]
