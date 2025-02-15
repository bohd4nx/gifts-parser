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

        try:
            with open(config_path, 'r', encoding='utf-8') as fp:
                config.read_file(fp)
        except FileNotFoundError:
            raise Exception(f"Config file not found at {config_path}")
        except Exception as e:
            raise Exception(f"Error reading config: {str(e)}")

        return config

    def _init_paths(self) -> None:
        self.BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        self.DATA_DIR = os.path.join(self.BASE_DIR, 'data')
        self.TEMP_DIR = os.path.join(self.BASE_DIR, 'temp')

    def _load_settings(self) -> None:
        self.BOT_TOKEN: str = self.config.get('Bot', 'TOKEN')
        self.LOCALE: str = self.config.get('Bot', 'LOCALE', fallback='RU').upper()
        if self.LOCALE not in ['RU', 'EN']:
            self.LOCALE = 'RU'
        self.ADMINS: List[int] = [
            int(admin.strip())
            for admin in self.config.get('Bot', 'ADMINS').split(',')
            if admin.strip()
        ]

        self.API_ID: int = self.config.getint('Telegram', 'API_ID')
        self.API_HASH: str = self.config.get('Telegram', 'API_HASH')

        self.BATCH_SIZE: int = self.config.getint('Parser', 'BATCH_SIZE')

    def _ensure_dirs(self) -> None:
        os.makedirs(self.TEMP_DIR, exist_ok=True)


config = Config()

BOT_TOKEN = config.BOT_TOKEN
BATCH_SIZE = config.BATCH_SIZE
ADMINS = config.ADMINS
API_ID = config.API_ID
API_HASH = config.API_HASH
BASE_DIR = config.BASE_DIR
DATA_DIR = config.DATA_DIR
TEMP_DIR = config.TEMP_DIR
LOCALE = config.LOCALE
