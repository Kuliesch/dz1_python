FROM postgres:16-alpine

ENV POSTGRES_DB=bluewave \
    POSTGRES_USER=bluewave \
    POSTGRES_PASSWORD=bluewave

COPY init/ /docker-entrypoint-initdb.d/
