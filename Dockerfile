FROM modamine/promotions-scrapper-base:latest

ENV APP_ENV=prod

WORKDIR /code

COPY backend/ /code
