import logging
from abc import ABC, abstractmethod

from doot.callback import BotCallback
from doot.response import HandlerResponse


class MessageHandler(ABC):

    def __init__(self, callback: BotCallback):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._callback = callback

    @abstractmethod
    def handle_message(self, message_text: str, chat_id: int) -> HandlerResponse:
        pass


class DefaultMessageHandler(MessageHandler):

    def __init__(self, callback: BotCallback):
        super().__init__(callback)

    def handle_message(self, message_text: str, chat_id: int) -> HandlerResponse:
        return HandlerResponse(message=f'Echo: {message_text}')
