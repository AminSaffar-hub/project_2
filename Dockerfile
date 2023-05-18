FROM modamine/promotions-scrapper-base:0.0.1

ENV APP_ENV=prod

WORKDIR /code

COPY backend/ /code
