from abc import ABC, abstractmethod

from aiogram.types import BotCommand


class BaseParser(ABC):
    @abstractmethod
    async def parse(self, *args, **kwargs):
        pass


class BaseDataHandler(ABC):
    @abstractmethod
    def process(self, *args, **kwargs):
        pass


class BaseManager(ABC):
    @abstractmethod
    async def initialize(self):
        pass

    @abstractmethod
    async def cleanup(self):
        pass


class BotCommands(ABC):
    @staticmethod
    async def setup_commands(bot):
        commands = [
            BotCommand(command="start", description="Start the bot"),
        ]
        await bot.set_my_commands(commands)
