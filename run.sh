docker build -t lazy .
docker run -p 80:8888 --volume=/home/ubuntu/lazy_prices/data:/home/jovyan/data lazy
