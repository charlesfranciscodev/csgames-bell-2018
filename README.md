# CSGames Bell 2018 - Practice

This repo is a web application project and uses Docker, Flask and React. 

## Start the server and the client
`./start.sh`

## Common Commands

Build the images:

`docker-compose -f docker-compose-dev.yml build`

Run the containers:

`docker-compose -f docker-compose-dev.yml up -d`

## Other Commands

To stop the containers:

`docker-compose -f docker-compose-dev.yml stop`

Remove images:

`docker rmi $(docker images -q)`

## Completed User Stories
* [BP:3] En tant qu'opérateur, je peux exécuter un seul script bash pour démarrer à la fois le serveur et le client

## Completed API Routes
* POST /bell/authentication
* PUT /bell/authentication
* GET /bell/assets?profiles=X&profiles=Y

## References
* [CSGames Bell 2018 - User stories (final - FR version)](https://trello.com/b/7oxDtTjm/csgames-bell-2018-user-stories-final-fr-version)
* [Microservices with Docker, Flask, and React](https://github.com/testdrivenio/testdriven-app-2.4)
