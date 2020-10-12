.PHONY: docker-run

docker-build:
	docker build -t overdose-analysis .

setup-dirs:
	mkdir -p logs
	mkdir -p data

docker-run: docker-build setup-dirs
	docker run \
	-v data:/var/app/data \
	-v logs:/var/app/logs \
	-e SOCRATA_TOKEN=${SOCRATA_TOKEN} \
	-t overdose-analysis
