image:
	docker build -t krobotkin-img .

start: image
	docker run -it --rm --name krobotkin-proc krobotkin-img
