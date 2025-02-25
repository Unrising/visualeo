FROM postgres:13

ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=crypto_db

COPY init.sql /docker-entrypoint-initdb.d/
