# Ten East
App demo using:
- docker
- poetry
- django
- postgres
- typescript
- pico css

## Requirements
 - Docker
 - Docker Compose

## Installation
```
docker compose up --build
```
App should be available at `localhost:8000`
## Features


```
docker compose exec db pg_dump -U myuser -d mydatabase > backup.sql

cat backup.sql | docker compose exec -T db psql -U myuser -d mydatabase

```
