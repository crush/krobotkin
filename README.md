# krobotkin

![Krobotkin](/docs/img/krobotkin.jpg)

_Image courtesy of [Emerican Johnson](https://twitter.com/emericanjohnson/status/1006515332696010753)_.

Krobotkin supports ranked voting for Discord as its primary function.

# Setup

In order to run krobotkin, the only thing you'll need is [Docker](https://www.docker.com).
All of the setup is handled via the [Makefile](./Makefile), which you'll need
[make](http://man7.org/linux/man-pages/man1/make.1.html) to run.

To run the bot, run the following command:

```
make start
```

At this point, you'll see Docker download the Python3.8 image and build krobotkin,
which will output the message "Anarchism is order."
