# [Nodejs Login App Container](https://hub.docker.com/r/adityajn105/node_loginapp)

A container that be extended for full-fledged login portal. 

Currently it provides a register/login system with photo uploads etc. vscode is running on port 5000 while application is hosted on port 3000.

## Dependencies
1. Requires a mongo server (DNS named 'mongo')

## Usage
You can use [docker-compose file](https://github.com/adityajn105/my_docker_files/blob/master/nodejs_loginapp/node_mongo_login_system.yaml) which will setup whole thing for you, change PASS in compose file to your password.:

	docker-compose -f node_mongo_login_system.yaml 

Alternatively you can run following commands to setup whole environment.

	docker pull adityajn105/node_loginapp:latest
	
	docker pull mongo
	
	docker network create node_network --driver bridge
	
	docker run -d --network node_network -v nodeapp-db:/data/db -v nodeapp-configdb:/data/configdb mongo:latest

	docker run -d -p 80:3000 -p 5000:5000 --network node_network -e PASS=password -v nodeapp-photodb:/home/node/profilephotos adityajn105/node_loginapp:latest

Get vscode in your browser by visiting `http://localhost:5000`.

## Contributors
* [Aditya Jain](https://adityajain.me)