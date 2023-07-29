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
        reply = ""
        reply_user = ""

        chatType: str = update.message.chat.type
        chatId: int = update.message.chat.id
        if update.message.reply_to_message:
            reply: str = update.message.reply_to_message.text
            reply_user: str = update.message.reply_to_message.from_user.username
        question: str = update.message.text

        userToken: str = JellyChatAPI.create_user_token(chatId)  # create user token

        # Add reply to question if reply exists
        if reply:
            question = f"{reply}\n\n{question}"

        print("----")
        print(f"Chat ID: {chatId}")
        print(f"Chat Type: {chatType}")
        if reply:
            print(f"Reply: {reply}")
            print(f"Reply User: {reply_user}")
        print(f"Question: {question}")
        print("----")

        # Differentiate between a group and a private chat
        if "group" in chatType:  # Group Chat
            if self.username in question or reply_user:
                replaced_text: str = question.replace(self.username, "").strip()
                answer: str = self.jellyChatAPI.user_message(userToken, replaced_text, JellyChatTelegramBot.APPLICATION)
            else:
                return
        else:  # Private Chat
            answer: str = self.jellyChatAPI.user_message(userToken, question, JellyChatTelegramBot.APPLICATION)

        print(f"--> Answer: {answer}")
        await update.message.reply_text(answer)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chatType: str = update.message.chat.type

        if chatType == "private":
            chatId: int = update.message.chat.id
            userToken: str = JellyChatAPI.create_user_token(chatId)  # create user token
            history = self.jellyChatAPI.user_history(userToken)
            if len(history) == 1:
                await update.message.reply_text(history[0].get("content"))
            else:
                await update.message.reply_text(f"Hey there!🪼\nI think I remember your face... "
                                                f"Sure you are: @{update.message.from_user.username}\n"
                                                f"Nice to have you back. If you have any question, "
                                                f"don't be shy and ask me something⁉️")


if __name__ == '__main__':
    load_dotenv()
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    bot = JellyChatTelegramBot(TELEGRAM_TOKEN, TELEGRAM_BOT_USERNAME)
    bot.run()
