.PHONY: all image start test

all: image start test

image:
	docker build -t krobotkin-img .

test-image:
	docker build -t krobotkin-test-img -f Dockerfile_test .

start: image
	docker run -it --rm --name krobotkin-proc krobotkin-img

test: test-image
	docker run -it --rm --name krobotkin-test-proc krobotkin-test-img
