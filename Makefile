REGISTRY?=quay.io
REPOSITORY?=fabric8-analytics/f8a-release-monitor
DEFAULT_TAG=latest
TESTS_IMAGE=f8a-release-monitor-tests

.PHONY: all docker-build fast-docker-build test get-image-name get-image-repository

all: fast-docker-build

docker-build:
	docker build --no-cache -t $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG) .

fast-docker-build:
	docker build -t $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG) .

fast-docker-build-tests:
	docker build -t f8a-release-monitor-tests -f Dockerfile .

test: fast-docker-build
	./runtest.sh

get-image-name:
	@echo $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG)

get-image-repository:
	@echo $(REPOSITORY)
