# discordbot

The official Discord bot for The Art of Tech: Not Playing With A Full Tech

## Building

First of all, rename the ".env.sample" file to ".env" in the project directory and set the `TOKEN` variable inside it to your Discord bot's token.

### Pip

```bash
# install dependencies
$ pip install -r requirements.txt

# run the bot
$ python main.py
```

### Docker

```bash
# using Docker Compose to build our custom image
$ docker-compose build

# running it
$ docker-compose up
```