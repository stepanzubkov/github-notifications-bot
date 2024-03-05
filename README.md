# Github Notifications Telegram bot

It is the telegram bot that shows your notifications from github.com. Bot is in beta stage.

## Deploy

For deployment you should create telegram bot at BotFather and install docker with docker-compose via your package manager.

1.
```
cd src
cp config_example.env config.env
```

2. Open `config.env` file and fill in your values for environment variables.
3. (I recommend you to use docker with docker-compose)
```
docker-compose build
docker-compose up
```
4. Check docker logs and then check the bot with `/start` command

## Using

Available commands:
- */start* - Standart start bot command. Prints info how to use.
- */login <github token>* - Login to your github account using *github api token*.
- */notifications* - Show unread notifications (login required).

## Contribution
Contributors are welcome! You can send issues and PRs.
