your_bot_token = "YOUR_TOKEN_HERE"

import re, logging
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    MessageHandler,
    filters,
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

unallowed_emojis = ['🇵🇸', '🇦🇪', '🇪🇬', '🇮🇷', '🇮🇶', '🇯🇴', '🇰🇼', '🇱🇧', '🇸🇦', '🇶🇦', '🇸🇾', '🇾🇪']

async def message_handler(update: Update, context: CallbackContext):
    message = update.message.text
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    username = update.message.from_user.username

    for emoji in unallowed_emojis:
        pattern = re.escape(emoji)
        if re.search(pattern, message):
            logger.info(f"Message from @{username} with blacklisted emojis at chat: {chat_id}")
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            await context.bot.send_message(chat_id=chat_id, text=f"@{username} has sent blacklisted emojis.")
            break
    
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