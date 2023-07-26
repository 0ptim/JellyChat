import os
import sys
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application, MessageHandler, filters

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from jellychatapi import JellyChatAPI


class JellyChatTelegramBot:
    APPLICATION: str = "telegram"

    def __init__(self, token: str, username: str):
        self.token = token
        self.username = username

        self.jellyChatAPI = JellyChatAPI()

        print("Initializing bots...")
        self.app = Application.builder().token(token).build()

        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))

        self.app.add_handler(MessageHandler(filters.TEXT, self.handler))

    def run(self):
        """
        Run the bot
        """
        print("Telegram bot has started...")
        self.app.run_polling(0.5)  # Check for messages every 0.5 seconds

    async def handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        This method handles all incoming messages for the bot:
        It will whether the message is coming from a private or a guild chat and acts accordingly
        """
        chatType: str = update.message.chat.type
        question: str = update.message.text
        chatId: int = update.message.chat.id

        userToken: str = JellyChatAPI.create_user_token(chatId)  # create user token

        print(f"User ({update.message.chat.id}) in {chatType}: '{question}'")

        # Differentiate between a group and a private chat
        if "group" in chatType:  # Group Chat
            if self.username.replace('\"', "") in question:
                replaced_text: str = question.replace(self.username, "").strip()
                answer: str = self.jellyChatAPI.user_message(userToken, replaced_text, JellyChatTelegramBot.APPLICATION)
            else:
                return
        else:  # Private Chat
            answer: str = self.jellyChatAPI.user_message(userToken, question, JellyChatTelegramBot.APPLICATION)

        print(f"Bot: {answer}")
        await update.message.reply_text(answer)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hey I'm Jelly 🪼 and I'm here to help you with everything around Defichain!\n"
                                        "Don't be shy and ask me something⁉️")

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("If there is something i can help you with, just ask!🙋🏻")


if __name__ == '__main__':
    load_dotenv()
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    bot = JellyChatTelegramBot(TELEGRAM_TOKEN, TELEGRAM_BOT_USERNAME)
    bot.run()
