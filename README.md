# CSGames Bell 2018

This repo is a web application project and uses Docker, Flask and React. 

## Competition Description
You are an extraterrestrial life form on Earth without any tools to properly integrate yourself. What's better than news shows and TV shows to open a conversation with humans?

The goal:
Your task is to create a streaming platform (HTTP REST backend and web frontend) to provide easy access to human content for extraterrestrial life form. You have been given a set of stories with business points for each story. The more business points you complete, the better extraterrestrials will be able to integrate on Earth.

## Start the server and the client
`./start.sh`

The client should be acessible at [http://localhost:3007/](http://localhost:3007/)

## Common Commands

Build the images:

`docker-compose -f docker-compose-dev.yml build`

Run the containers:

`docker-compose -f docker-compose-dev.yml up -d`

Create the database:

`docker-compose -f docker-compose-dev.yml exec server python manage.py recreate_db`

Seed the database:

`docker-compose -f docker-compose-dev.yml exec server python manage.py seed_db`

## Other Commands

To stop the containers:

`docker-compose -f docker-compose-dev.yml stop`

Remove images:

`docker rmi $(docker images -q)`

## Postgres
Want to access the database via psql?

`docker-compose -f docker-compose-dev.yml exec database psql -U postgres`

## Client
Connect to the client

`docker-compose -f docker-compose-dev.yml exec client /bin/sh`

## Completed User Stories
* [BP:3] As an operator, I can run a bash script that starts both the client and the server
* [BP:8] As an extraterrestrial user, I can navigate through available assets
* [BP:2] As an extraterrestrial user, I am able to search content

## Completed Required API Routes
* **POST** `/bell/authentication`
* **PUT** `/bell/authentication`
* **GET** `/bell/assets?profiles=X&profiles=Y`
* **GET** `/bell/alerts`
* **PUT** `/bell/hidden/provider/{:id}/refreshRate`
* **PUT** `/bell/hidden/asset/{:id}`
* **POST** `/bell/hidden/account`
* **GET** `/bell/search?query=<query>`

## Completed Additional API Routes

**GET** `/bell/asset/<:id>`

Returns the asset which corresponds to the media id parameter, only if the current date is within the licensing window.

Response
```json
{
  "title" : "My dog Chop",
  "providerId": "HBO",
  "refreshRateInSeconds": 5,
  "media": {
    "mediaId": "fH5yKr_c62A",
    "durationInSeconds": 15
  }
}
```
200 | when the asset is valid

400 | when the media id or licensing window is invalid

---

**POST** `/bell/logout/`

Logs out the currently logged in user.

Response
```json
{
  "message": "Logout successful"
}
```
200 | Logout successful

## Profiles
| profile_id | name |
|:----------:|:----:|
| 1 | Pirate |
| 2 | Mac User |
| 3 | Vaporwave Lover |
| 4 | Deaf |
| 5 | Hipster |
| 6 | Robot |
| 7 | Uniped |
| 8 | 3D Enthusiast |
| 9 | Simpsons Enthusiast |

## References
* [CSGames Bell 2018 - User stories (final - EN version)](https://trello.com/b/pT20udUF/csgames-bell-2018-user-stories-final-en-version)
* [Microservices with Docker, Flask, and React](https://github.com/testdrivenio/testdriven-app-2.4)
* [React + Redux - User Registration and Login Tutorial & Example](http://jasonwatmore.com/post/2017/09/16/react-redux-user-registration-and-login-tutorial-example)
