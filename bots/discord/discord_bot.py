import os
import sys
import logging
from dotenv import load_dotenv

import discord

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from jellychatapi import JellyChatAPI
from logger import configure_logging


configure_logging()


class JellyChatDiscordBot(discord.Client):
    APPLICATION: str = "discord"

    def __init__(self):
        self.jellyChatAPI = JellyChatAPI()

        logging.info("Initializing bots...")
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        """
        This method will log if the bot has stared successfully and list all connected guilds
        """
        logging.info("The Discord bot is up and running...")
        logging.info("The Discord Bot is running on the following servers: ")
        for guild in self.guilds:
            logging.info(f"\t{self.guilds.index(guild)}: {guild.name}")

    async def on_message(self, message):
        """
        This method handles all incoming messages for the bot:
        It will whether the message is coming from a private or a guild chat and acts accordingly
        """
        # Ignore message from the bot himself
        if message.author == self.user:
            return

        # Distinguish between private and guild chat
        if isinstance(message.channel, discord.DMChannel):
            await self.private(message)
        else:
            await self.guild(message)

    async def guild(self, message):
        """
        This method handles all messages of a guild chat:
        The Bot only answers if he is tagged
        """
        # Only generates and sends message if bot is tagged
        reply = None
        if message.reference:
            reply = await self.fetch_message(message, message.reference.message_id)

        if self.user in message.mentions:
            answer: str = self.get_answer(message, is_private=False, reply=reply)
            await self.send(message, answer, is_private=False)

    async def private(self, message):
        """
        This method handles all messages of a private chat:
        It will always answer on anything that has been written into the chat
        """
        await self.is_first_message(message)
        answer: str = self.get_answer(message, is_private=True)
        await self.send(message, answer, is_private=True)

    def get_answer(self, message, is_private: bool, reply=None):
        """
        This method queries an answer for the asked question
        """
        # Private chat identification: author name
        # Guild chat identification: guild name + channel name
        userToken: str = JellyChatAPI.create_user_token(message.guild.name + message.channel.name
                                                        if not is_private else message.author.name)

        # Prompt that is appended to the question.
        extra_prompt = " The answer must be less than 2000 characters in length."

        message_content: str = message.content.replace(f"<@{self.user.id}>", "")  # + extra_prompt

        if reply:

            reply_content: str = reply.content.replace(f"<@{self.user.id}>", "")
            logging.info(f"Question: User: {message.author.name}, Reply:\n{reply_content}\nQuestion:\n{message_content}")
            question: str = f"{reply_content}\n\n{message_content}"
        else:
            question: str = message_content
            logging.info(f"Question: User: {message.author.name}, Question:\n{message_content}")

        answer: str = self.jellyChatAPI.user_message(userToken, question, JellyChatDiscordBot.APPLICATION)
        logging.info(f"Answer: User: {message.author.name}, Answer: {answer}")
        return answer

    async def send(self, message, answer, is_private: bool):
        """
        This method sends the answer either into the guild or private chat
        """
        try:
            if is_private:
                await message.author.send(answer, reference=message)
            else:
                await message.channel.send(answer, reference=message)
        except Exception as e:  # An error will occur if the answer is longer than 2000 characters
            logging.error(f"There is an error sending the message: {e}")
            msg = "Woooops, something went wrong while trying to ship the answer to you."
            if is_private:
                await message.author.send(msg, reference=message)
            else:
                await message.channel.send(msg, reference=message)

    async def is_first_message(self, message):
        userToken: str = JellyChatAPI.create_user_token(message.author.name)
        history = self.jellyChatAPI.user_history(userToken)
        # If new user --> load context user message
        if len(history) == 1:
            logging.info(f"New User: {message.author.name}")
            await message.author.send(history[0].get("content"))

    async def fetch_message(self, ctx, message_id: int):
        try:
            # Fetch the message from the channel using the message_id
            message = await ctx.channel.fetch_message(message_id)
            return message
        except discord.NotFound:
            logging.error("Message not found.")
        except discord.Forbidden:
            logging.error("Bot doesn't have permission to access the message.")
        except discord.HTTPException:
            logging.error("An error occurred during the HTTP request.")


if __name__ == '__main__':
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

    app = JellyChatDiscordBot()
    app.run(DISCORD_TOKEN)
