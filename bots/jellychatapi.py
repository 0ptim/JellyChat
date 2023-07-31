import requests
import hashlib
import logging
from typing import Any


class JellyChatAPI:

    @staticmethod
    def create_user_token(identification: Any) -> str:
        return hashlib.sha256((str(identification)).encode("utf-8")).hexdigest()

    @staticmethod
    def get_response(response):
        if "response" in response:
            return response.get("response")
        else:
            logging.error(f"There is an error with the connection to JellyChat API")
            return f"Hey here is Jelly. I'm sleeping right now!💤"

    def __init__(self, url: str = "https://jellychat.fly.dev"):
        self.url = url

    def user_message(self, userToken: str, message: str, application):
        try:
            self.user_history(userToken)
            return JellyChatAPI.get_response(requests.post(self.url + "/user_message",
                                                           json={"user_token": userToken, "application": application,
                                                                 "message": message}).json())
        except Exception as e:
            logging.error(f"Failing connection to API {self.url}: \n{e}")
            return f"Hey here is Jelly. I'm sleeping right now!💤"

    def user_history(self, userToken: str) -> [{}]:
        return requests.post(self.url + "/history", json={"user_token": userToken}).json()


if __name__ == "__main__":
    pass
