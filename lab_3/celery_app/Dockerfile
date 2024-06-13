FROM python:3.10-alpine3.19

WORKDIR /celery_app

COPY . .
RUN pip3 install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8002