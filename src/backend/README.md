# How to Set Up

## Set Up with Docker 
If you already have Docker and docker-compose installed on your local environment, you can directly use the following command to build and start the project. (Make sure your Docker Daemon is running)
```Shell
chmod +x run.sh
./run.sh
```

Otherwise, please follow the instructions at https://docs.docker.com/get-docker/ to get Docker and docker-compose (Mac and Windows users do not need to install it separately, it is already built into the Docker application).

When you see the following log information, it means that you have successfully started the project and ready to access the website in http://localhost:8000.
```Shell
educationx_backend  | Watching for file changes with StatReloader
```

After that, you can modify your code normally and all changes will be updated to the Docker container.

## Customize Docker configuration and environment variables
Please follow comments in `docker-compose.yml` and `Dockerfile` to configure your Docker configuration.
For environment variables, you can modify them in `.env` file.

## How to stop
Using `Cltr-C` or `CMD-C` to kill the `run.sh` process can stop the docker container and project.
You can also stop it in Docker Desktop GUI.

## Common docker and docker-compose commands
* `docker image ls`:  list all docker images
* `docker image rm [option] <image1> [<image2> ...]`: remove images
* `docker-compose up`: run docker containers specified by `docker-compose.yml` file
* `docker-compose up -d`: run containers in background
* `docker-compose stop`: stop all containers specified by `docker-compose.yml` file
* `docker-compose down`: stop and remove all containers specified by `docker-compose.yml` file