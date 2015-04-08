### Installation steps
#### 1. [Install docker](https://docs.docker.com/installation/)
#### 2. Start the redis server
    docker run -d --name redis -p 6379:6379 dockerfile/redis
#### 3. Build the image from the Dockerfile
    docker build -t cloud .
#### 4. Run the script
    docker run --rm=true --name cloud --link redis:redis cloud python /src/words-cloud.py <seconds> <cloud-size>

    Where:
      <seconds> - The duration of the data fetch process
      <cloud-size> - The number of words included in the tag cloud
