# block_arab for Telegram
This is a python-telegram-bot to handle/filter sent messages that contain any Arabic letters or country emojis. 

# Installation

You can run this bot on your own, install the required lib by running this command: 

```bash
pip install python-telegram-bot
```

First line in the `main.py` file you will find the bot token variable, get your bot's token from the [BotFather](https://telegram.me/botfather) and insert it in the code:

```python
your_bot_token = "YOUR_TOKEN_HERE"
```

These are the current emojis/flags that are being blacklisted:

```python
['🇵🇸', '🇦🇪', '🇪🇬', '🇮🇷', '🇮🇶', '🇯🇴', '🇰🇼', '🇱🇧', '🇸🇦', '🇶🇦', '🇸🇾', '🇾🇪']
```
