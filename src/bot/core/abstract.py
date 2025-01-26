from abc import ABC, abstractmethod


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
