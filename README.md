# MY Docker Files for Automated build

Visit [My DockerHub Account](https://hub.docker.com/u/adityajn105)

Build List
1. [deeplearning](https://hub.docker.com/r/adityajn105/deeplearning)
2. [nodejs_loginapp](https://hub.docker.com/r/adityajn105/node_loginapp)
3. [digit_recongizer_app](https://hub.docker.com/r/adityajn105/digit_recognizer_app)
4. [ner_pos_tagging_app](https://hub.docker.com/r/adityajn105/ner_pos_tagging_app)






## Basic Commands

### Container related
* Some tips

    1. container's host name defaults to container name
    2. If you specify CMD, it will override Images' Dockerfile CMD
    3. -v use named volumes or mount binds to save container data.
    4. Use custom bridge network when container is interacting with other network

* to run a container (-d detach), (-v volume/mount), (-e environment_var)

        docker container run -d --name myCont -p 80:80 -v ${pwd}:/home/local --network myNetwork -e PASSWORD=aditya image:tag CMD 

* to start stopped container

        docker container start -d myCont

* To execute a command on running container

        docker container exec -d myCont CMD

* To stop or remove (-f force-remove) a container

        docker container stop/rm -f myCont1 myCont2

* To list all runnning container (-a for all including stopped ones)

        docker container ls -a

* To inspect a container (gives networks, volumes, ip etc)

        docker container inspect myCont

* To view open ports

        docker container port myCont

### Networking related 

* There are 3 types of network: 
    1. bridge - all devices on network can access each other . 
    2. host - everyone can access each other. (skip complexity but becomes unsecure)
    3. None - not connected to any network (like a standlone computer) 

* Always use a custom bridge network when working with more than 2 container (one container can 1+ network)

        docker network create --driver bridge myNetwork

* To list all networks

        docker network ls

* To inspect a network (node attached to it with their IP)

        docker network inspect myNetwork

* To attach a container to a network

        docker network connect myNetwork myContainer

* To detach a container from a network

        docker network disconnect myNetwork myContainer

* We can assign same network-alias to more than 2 container while creating, This will act as DNS for both container and will serve in a round robin fashion.

        docker container run --name myCont --network myNetwork --network-alias search elasticsearch:2


### Image related
* Image are application binaries with required dependencies without kernel and with instructions on how to run image. To pull a image.

        docker image pull user/repo:tag

* Images are not huge blob of data but are made up of layers. To see all layers.

        docker image history myImage

* List all images

        docker image ls

* Inspect a image, gives open ports, CMD etc

        docker image inspect myImage

* To build a image from its Dockerfile (-f to use custom name)

        docker image build -t user/repo:tag -f Dockerfile .

* To tag a image with different name or tag

        docker image tag user/repo:tag user2/repo2:tag2

* To push image into registry

        docker image push user/repo:tag

* To remove a image from local

        docker image rm user/repo:tag

* To remove all dangling images

        docker image prune

### Volumes related

* To list all volumes (default names are SHA use named-volumes)

        docker volume ls

* To assign a named volume while running a container

        docker container run -d -v mysql-db:/var/lib/mysql mysql

* To assign a mount bind, this is path on host PC shared between host and docker container. (${PWD} for win power-shell)

        docker container run -d -v $(pwd):/home/local myImage

* To remove a named volume

        docker volume rm vol-name[/sha]

* To inspect a volume, to see original path

        docker volume inspect vol-name[/sha]

### Docker Compose
* Tips
    1. To build a working application with one or more container for development purposes 
    2. uses a docker compose file
    3. If you are using named-volumes or networks create them at bottom in compose-file.


* To run an application using docker compose file (-f filename for compose file)

        docker-compose up -f filename

* To stop and remove whole application ( named volumes have to deleted manually or use -v flag )

        docker-compose down -v


### Docker Swarm
* Tips:
    1. It is container orchestrater. Use it for deploying whole application for production with inbuilt load balancing and fault taulerence.
    2. There are services which can be thought of as a containers, there can be multiple replicas for each service and load balancing is done by swarm itself.
    3. Container two types of nodes- Manager/Worker. Manger assign work services to itself and other workers. Whole system works on consensus of manager nodes. So keep odd number of manager nodes.
    4. Every service can be accessed from every node or thier IP in swarm. This is done by routing Mesh which uses a overlay network. It is like a virtual IP in from of service.
    5. Use docker stack to automate whole process. It is like a docker compose but for production.

* To initialize a swarm on node, this will be a Manger(leader) node. Use advertise-addr in cloud for public ip.

        docker swarm init --advertise-addr <public-ip>

* Run command given by running following command on other nodes to add them as manager/worker.

        docker swarm join-token manager/worker

* To view all nodes with their roles

        docker node ls

* To create a service with 3 replicas

        docker service create --name myService --replicas 3 myImage:2.0

* To list all services with number of replicas running

        docker service ps

* To show service is running on which node

        docker service ps mySerive

* To update a service (see more update options like add/remove port on docs)

        docker service update --replicas 5 --image myImage:2.1  myService

* To remove a service

        docker service rm myService