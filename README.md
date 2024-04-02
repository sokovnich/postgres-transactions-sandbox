# postgres-transactions-sandbox

On Ubuntu:
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
apt install docker-compose-plugin

docker compose up

curl http://127.0.0.1:5000/init_db

curl http://127.0.0.1:5000/create_error
curl http://127.0.0.1:5000/create_error2
...
```