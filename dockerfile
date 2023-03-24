FROM python:3.9.16-slim-buster
WORKDIR /gamestart

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY ./app /gamestart/app
COPY ./alembic /gamestart/alembic
COPY ./alembic.ini /gamestart/alembic.ini
COPY ./requirements.txt /gamestart/requirements.txt

RUN pip install -r requirements.txt
CMD [ "uvicorn", "app.main:app",  "--host", "0.0.0.0", "--port", "80"]