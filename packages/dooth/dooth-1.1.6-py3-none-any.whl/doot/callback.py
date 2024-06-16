from abc import ABC

from doot.message import Update
from doot.response import HandlerResponse


class BotCallback(ABC):
    """
    Callback interface to send partial update messages to chat from CommandHandler
    and MessageHandler.
    """
    def interim_response(self, response: HandlerResponse, chat_id: int):
        pass