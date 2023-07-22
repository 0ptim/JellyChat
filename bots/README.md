# JellyChat Bots

## Build and run bots with docker

### Telegram Bot

Build:
```bash
docker build -t jelly_chat_telegram_bot -f telegram/Dockerfile .
```
Run:
```bash
docker run --name JellyChatTelegramBot --env-file .env -d jelly_chat_telegram_bot
```

### Discord Bot

Build:
```bash
docker build -t jelly_chat_discord_bot -f discord/Dockerfile .
```
Run:
```bash
docker run --name JellyChatDiscordBot --env-file .env -d jelly_chat_discord_bot
```