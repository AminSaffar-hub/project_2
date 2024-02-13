# backend
## Requirements
- python 3.9
- poetry: https://python-poetry.org/docs/#installing-with-the-official-installer

## Installation
run the following command:
```bash
poetry install
```

## Running the backend
```bash
poetry run python manage.py runserver.py
```
or if you set up virtual env with vsCode
```bash
source .venv/bin/activate
./manage.py runserver.py
```

api docs should be available on: http://localhost:8080/api/docs
admin should be available on: http://localhost:8080/admin

contact staff members for password.

## Running scrapy spiders

to run all spiders:
```bash
cd backend;
./manage.py crawl
```

to run a specific spider:
```bash
cd backend;
./manage.py crawl --spider <spider-name>
```
