### Installation steps
#### 1. [Install docker](https://docs.docker.com/installation/)
#### 2. [Install docker-compose](https://docs.docker.com/compose/install/)
#### 3. Start the Docker daemon
    docker -H 0.0.0.0:2375 -d &
#### 4. Set the DOCKER_HOST environment variable
    export DOCKER_HOST="tcp://127.0.0.1:2375"
#### 5. Create and start the containers
    docker-compose up -d
 	Note: This is mostly for the Redis container. Considering that the cloud app it's a script and it also takes command line arguments we better start it with a one-off command (step 6).
#### 6. Run the script
    docker-compose run cloud python words-cloud.py <seconds> <cloud-size>
    Where:
        - <seconds> - The duration of the data fetch process
        - <cloud-size> - The number of words included in the tag cloud

