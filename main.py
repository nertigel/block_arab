your_bot_token = ""

import re
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    MessageHandler,
    filters,
)

async def message_handler(update: Update, context: CallbackContext):
    message = update.message.text
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    print(f"Received message: {message}")

    if re.search('[\u0600-\u06FF]', message):
        await context.bot.send_message(chat_id=chat_id, text=f"A terrorist sent a message: {message}")
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(your_bot_token).build()
    
    __handlers__ = {}
    __handlers__["restrict_keywords"] = MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler)

    for name, handler in __handlers__.items():
        print(f'Adding handler {name}')
        application.add_handler(handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()