your_bot_token = ""

import re, logging, time
from logging.handlers import RotatingFileHandler
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    MessageHandler,
    filters,
)
# log format for logger
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# logger
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger() # change to logging.getLogger(__main__) for less debug information

# log file name
timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
log_file_name = f'{timestamp}.log'

# formatter to redact the token
class redact_token(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        if your_bot_token in message:
            message = message.replace(your_bot_token, '[TOKEN]')
        return message

# create log file
file_handler = RotatingFileHandler(log_file_name, maxBytes=1e6, backupCount=3)
file_handler.setFormatter(redact_token(log_format))
logger.addHandler(file_handler)

# stream cli to log
console_handler = logging.StreamHandler()
console_handler.setFormatter(redact_token(log_format))
logger.addHandler(console_handler)

unallowed_emojis = ['🇵🇸', '🇦🇪', '🇪🇬', '🇮🇷', '🇮🇶', '🇯🇴', '🇰🇼', '🇱🇧', '🇸🇦', '🇶🇦', '🇸🇾', '🇾🇪']

async def message_handler(update: Update, context: CallbackContext):
    message = update.message.text
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    username = update.message.from_user.username

    # search emojis
    for emoji in unallowed_emojis:
        pattern = re.escape(emoji)
        if re.search(pattern, message):
            logger.info(f"Message from @{username} with blacklisted emojis at chat: {chat_id}")
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            await context.bot.send_message(chat_id=chat_id, text=f"@{username} has sent blacklisted emojis.")
            break
    
    # search letters
    if re.search('[\u0600-\u06FF]', message):
        logger.info(f"Message from @{username} with blacklisted characters at chat: {chat_id}")
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await context.bot.send_message(chat_id=chat_id, text=f"@{username} has sent blacklisted characters.")

def main() -> None:
    """Run the bot."""
    if your_bot_token == "":
        logger.error("No token defined. Please change the string value of `your_bot_token`")
        return
    
    logger.info("Starting the bot")
    application = Application.builder().token(your_bot_token).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    application.run_polling()
    logger.info("ded")

if __name__ == "__main__":
    main()