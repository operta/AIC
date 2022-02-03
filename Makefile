start:
	docker-compose up --build -d

add_worker:
	docker build -t g7t3_worker worker && docker run --rm --network g7t3-network -e "CONTROLLER_URL=http://controller:5000" -e "WORKER_ID=7" -e "PORT=8187" -e "HOST=worker7" -p 8187:8187 --name worker7 g7t3_worker

restart:
	docker-compose restart

build:
	docker-compose build

purge:
	docker-compose down -v --rmi all --remove-orphans