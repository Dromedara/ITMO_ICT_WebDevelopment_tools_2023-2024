# Лабораторная 3

## Структура

```plaintext
project/
│
├── taskmanager/ (первая лабораторная)
│   └── ...
│
├── endpoints/ (парсер из второй лабораторной)
│   └── ...
│
├── docker-compose.yaml
└── .env

```


## docker 

### docker-compose

```python
version: '3.10'
services:

  taskmanager:
    container_name: taskmanager
    build:
      context: ./taskmanager
    env_file: .env
    depends_on:
      - db
    ports:
      - "8000:8000"
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    networks:
      - backend_3
    restart: always

  celery_app:
    container_name: celery_app
    build:
      context: ./celery_app
    env_file: .env
    restart: always
    ports:
      - "8002:8002"
    command: uvicorn main:app --host 0.0.0.0 --port 8002
    depends_on:
      - redis
      - db
    networks:
      - backend_3

  celery_start:
    build:
      context: ./celery_app
    container_name: celery_start
    command: celery -A celery_start worker --loglevel=info
    restart: always
    depends_on:
      - redis
      - celery_app
      - db
    networks:
      - backend_3

  redis:
    image: redis
    ports:
      - "6379:6379"
    networks:
      - backend_3
    depends_on:
      - db

  db:
    image: postgres
    restart: always
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=web_data
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - "5432:5432"
    networks:
      - backend_3


volumes:
  postgres_data:

networks:
  backend_3:
     driver: bridge
```

### Dockerfile (taskamanger)

```python
FROM python:3.10-alpine3.19

WORKDIR /taskmanager

COPY . .
RUN pip3 install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8000
```

### Dockerfile (celery_app)
```python
FROM python:3.10-alpine3.19

WORKDIR /taskmanager

COPY . .
RUN pip3 install -r requirements.txt

CMD uvicorn main:app --host localhost --port 8002
```

## Сelery

```python
celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_routes={
        "parse.parse_and_save": "main-queue",
    },
)

```


### Функция таски

```python
import requests
from bs4 import BeautifulSoup
from models import Parce
from celery_main import celery_app


@celery_app.task
def parse_and_save(url,  session):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No title'

    new_article = Parce(
        url = url,
        article_title = title
    )

    session.add(new_article)
    session.commit()
```

