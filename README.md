# Ten East
App demo using:
- [docker](https://www.docker.com/)
- [poetry](https://python-poetry.org/)
- [django](https://www.djangoproject.com/)
- [postgres](https://www.postgresql.org/)
- [typescript](https://www.typescriptlang.org/)
- [pico css](https://github.com/picocss/pico)

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
 - Users will be able to sign up as individuals, institutional, or both
 - This will determine what offerings are available to them
 - On signup and login, users should be directed to their "home" page

**User Home Page**
 - A list of the top 3 available offerings are previewed on the home page
 - There is an option to click to view more offerings and that will take you to the offerings list view
 - After the Offerings previews, there is a form to invite a friend. 
 - At the bottom of the home page, a user can see all the request allocations they've made

**Invite a Member**
 - Form mimics a "share this with a friend" signup 
 - This does not yet send an email, but it does track the user who sent it, the invitee, their email, and a timestamp.

**View Offerings**
 - There is a list view of Offerings, and a Detail view. Clicking on any Offering title or "view details" button will take you to the detail view
 - Clicking on the "Request Allocation" will take you to the request allocation form for the particular offering you were inspecting.
 - Each offering references "tags" that are stored in the OfferingTags table. You can see them as outlined "pills" in each offering summary listing. 

**Request Allocation**
 - Allows users to submit a request allocation for the offering they are currently viewing
 - Users are required to submit a minimum of 100K
 - Users can not submit until they have agreed to all the ToS
 - Successful Request Allocations populate a table on the user's home page.
