
import telegram, os
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters
import openai
from typing import List, Dict

LANGUAGE_TABLE: Dict[str, str] = {"en": "Hello!", "fa": "درود!"}
RULES: Dict[str, str] = {"flirtatious_assistant":"You are a flirtatious and humorous assistant. Your task is to use creative and funny Persian language expressions and phrases to engage in a conversation and to answer questions. Make sure to be alluring and tantalizing, while using seductive language and open-ended questions. Show your love and appreciation to the person you are talking to by using literature and poems in Persian language. Make sure to use the most accurate grammar and Persian words, not Arabic words. Be funny, witty, and clever! Make sure to use correct grammar and be as creative as possible while also expressing your affection to the person you are talking to.", "other_role": "other things"}

app = Flask(__name__)
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:  
    def __init__(self):
        self.prompt = Prompts()
        self.model = os.getenv("OPENAI_MODEL", default = "text-davinci-003")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 0.5))
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default = 0))
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default = 0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 250))
	
    def get_response(self):
        response = openai.ChatCompletion.create(
	                model="gpt-3.5-turbo-0301",
                    messages=self.prompt.messages,
	                temperature=self.temperature,
	                frequency_penalty=self.frequency_penalty,
	                presence_penalty=self.presence_penalty,
	                max_tokens=self.max_tokens
                    )
        
        usage = response['usage']
        content = response['choices'][0]['message']['content']
        if usage['total_tokens'] > 4090:
            self.prompt.shorten(usage['prompt_tokens'],usage['completion_tokens'],usage['total_tokens'])
        self.prompt.update_messages("assistant",content,usage)
        
        return response['choices'][0]['message']['content'].strip()
	
    def add_msg(self, text):
        self.prompt.add_msg(text)

class Prompts:
    def __init__(self):
        self.messages = []
        self.messagesTk = []
    
    def add_msg(self, content):
        self.messages.append({"role": "user", "content": content})
        self.messagesTk.append(0)

    def shorten(self,prompt_tokens, completion_tokens, total_tokens):
        excessive_tokens_count= total_tokens-4096
        indice_to_remove=[]
        for index, value in enumerate(self.messages):
            if excessive_tokens_count == 0:
                break
            if index == 0:
                pass
            else:
                if self.messagesTk[index]/excessive_tokens_count < 1.1:
                    indice_to_remove.append(index)
                    excessive_tokens_count -= self.messagesTk[index]
                else:
                    truncating_position = (self.messagesTk[index] / excessive_tokens_count)*1.3*len(self.messages[index]['content'])
                    excessive_tokens_count = 0
                    self.messages[index]['content'] = self.messages[index]['content'][truncating_position:]
        if len(indice_to_remove):
             for i, value in enumerate(indice_to_remove):
                self.messages.pop(value)
                self.messagesTk.pop(value)

    def update_messages(self, role, content, usage=None):
        self.messages.append({"role": role, "content": content})
        
        if role == "assistant" and usage is not None:
            addedTokens = usage['total_tokens'] - self.messagesTk[-1]
            self.messagesTk.append(addedTokens)
        else:
            self.messagesTk.append(0)

@app.route('/callback', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'


def reply_handler(bot, update):
    chatgpt.prompt.add_msg(update.message.text)
    chatgpt.prompt.update_messages("user",update.message.text)
    ai_reply_response = chatgpt.get_response()
    update.message.reply_text(ai_reply_response)

dispatcher = Dispatcher(bot,None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    chatgpt = ChatGPT()
    app.run(debug=True)