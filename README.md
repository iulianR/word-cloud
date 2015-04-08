docker run -d --name redis -p 6379:6379 dockerfile/redis

sudo docker build -t cloud .
docker run --name cloud --link redis:redis cloud
