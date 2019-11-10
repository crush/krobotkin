# krobotkin

![Krobotkin](/docs/img/krobotkin.jpg)

_Image courtesy of [Emerican Johnson](https://twitter.com/emericanjohnson/status/1006515332696010753)_.

Krobotkin supports ranked voting for Discord as its primary function.

# Setup

In order to run krobotkin, the only thing you'll need is [Docker](https://www.docker.com).
All of the setup is handled via the [Makefile](./Makefile), which you'll need
[make](http://man7.org/linux/man-pages/man1/make.1.html) to run.

The `make start` command will download the Python3.8 Docker image, build krobotkin,
and then run the bot in a Docker container.

# Testing

The `make test` command will invoke the project's unit and integration tests in a
Docker container built from a separate image from the one created to run the bot in.
