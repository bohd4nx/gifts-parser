import configparser
import os
from typing import List


class Config:

    def __init__(self):
        self.config = self._load_config()
        self._init_paths()
        self._load_settings()
        self._ensure_dirs()

    @staticmethod
    def _load_config() -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')

        if not config.read(config_path):
            raise FileNotFoundError(
                f"Configuration file not found at {config_path}. "
                "Please create config.ini in the root directory."
            )
        return config

    def _init_paths(self) -> None:
        self.BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        self.DATA_DIR = os.path.join(self.BASE_DIR, 'data')
        self.TEMP_DIR = os.path.join(self.BASE_DIR, 'temp')

    def _load_settings(self) -> None:
        self.BOT_TOKEN: str = self.config.get('Bot', 'TOKEN')
        self.ADMINS: List[int] = [
            int(admin.strip())
            for admin in self.config.get('Bot', 'ADMINS').split(',')
            if admin.strip()
        ]

        self.API_ID: int = self.config.getint('Telegram', 'API_ID')
        self.API_HASH: str = self.config.get('Telegram', 'API_HASH')

    def _ensure_dirs(self) -> None:
        os.makedirs(self.TEMP_DIR, exist_ok=True)


config = Config()

BOT_TOKEN = config.BOT_TOKEN
ADMINS = config.ADMINS
API_ID = config.API_ID
API_HASH = config.API_HASH
BASE_DIR = config.BASE_DIR
DATA_DIR = config.DATA_DIR
TEMP_DIR = config.TEMP_DIR
