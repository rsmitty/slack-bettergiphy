# slack-bettergiphy

A bot for Slack that will retrieve a single, relevant result from giphy, as opposed to the random pick that the built-in bot does.

Installation:

- Git clone this directory.

- Ensure that you have docker and docker-machine installed and configured.

Running:

- Configure a Slack slash command to talk to http://$IPADDRESS_OF_DOCKER_HOST:5000

- Configure an incoming webhook in Slack and take note of the webhook URL.

- Edit the variables slacktoken and slackhookurl in giphybot.py

- Build the docker container with:
`docker build -t rsmitty/giphy .`

- Run it with:
`docker run -p 5000:5000 --detach=true rsmitty/giphy`
