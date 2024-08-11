# Ten East
App demo using:
- docker
- poetry
- django
- postgres
- typescript
- pico css

## Requirements

## Installation

## Features


```
docker compose exec db pg_dump -U myuser -d mydatabase > backup.sql

cat backup.sql | docker compose exec -T db psql -U myuser -d mydatabase

```

* share with a friend just makes a share record in db