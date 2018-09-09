docker create -v /data --name relay-data busybox /bin/true

docker run --name relay --restart=always \
    -p 80:80 \
    -e INFURA_API_KEY=KZSQapS5wjr4Iw7JhgtE \
    --volumes-from relay-data \
    -v /home/aecc/ethberlin:/app \
    -d aecc/relay
#TODO: chmod 777 /data/*.db
