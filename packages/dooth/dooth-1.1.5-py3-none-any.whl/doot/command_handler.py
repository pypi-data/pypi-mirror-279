import logging
from abc import ABC, abstractmethod

from doot.callback import BotCallback
from doot.response import HandlerResponse


class CommandHandler(ABC):

    def __init__(self, callback: BotCallback):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._callback = callback

    @abstractmethod
    def handle_command(self, command: str, args: list, chat_id: int) -> HandlerResponse:
        pass


class DefaultCommandHandler(CommandHandler):

    def __init__(self, callback: BotCallback):
        super().__init__(callback)

    def handle_command(self, command: str, args: list, chat_id: int) -> HandlerResponse:
        return HandlerResponse(message=f'Command: {command}\nArgs: {args}')
