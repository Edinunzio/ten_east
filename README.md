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
```docker compose up --build```

App should be available at `localhost:8000`

### Creating superuser
```docker compose exec web python manage.py createsuperuser```

## Running Tests
Once a container has been built and is up, run the following:
```docker compose exec web pytest```


## Features
**Signup, Login, Logout**

**Invite a Member**

**Request Allocation**




### Special Notes
There have been decisions made considering the scope and goal of the project that I would normally handle differently in a production setting. The overall goal is for an easy to use demo of a web application that demonstrates my skills with regards to full stack web development, software design, and overall adherence to best practices in software engineering.

**Settings**
I typically have a base settings that is then imported in to a dev or prod settings. The credentials would not be hard coded like they are in this docker compose and `settings.py`. There would be environment variables set and/or use of secrets and .env files. 

