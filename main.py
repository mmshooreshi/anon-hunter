import logging
import os
import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters
import chatgpt as ChatGPT

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
chatgpt = ChatGPT()

@app.route('/callback', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

def reply_handler(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    chatgpt.prompt.add_msg(update.message.text)
    chatgpt.prompt.update_messages("user", update.message.text)
    update.message.reply_text(chatgpt.get_response())

dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    app.run(debug=True)