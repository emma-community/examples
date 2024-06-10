build:
	docker build -t luebken/multicloud-keydb-demo:0.0.1 . 

keydb:
	docker run -p 6379:6379 --name keydb-server -d eqalpha/keydb keydb-server
	docker inspect --format '{{ .NetworkSettings.IPAddress }}' keydb-server 

run:
	docker run -p 5001:5000 -e CLIENT_ID=$(CLIENT_ID) -e CLIENT_SECRET=$(CLIENT_SECRET) -e REDIS_HOST=172.17.0.2 luebken/multicloud-keydb-demo

push: 
	docker push luebken/multicloud-keydb-demo:0.0.1