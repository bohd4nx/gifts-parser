import configparser
import os


class Config:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        self.DATA_DIR = os.path.join(self.BASE_DIR, 'data')
        self.TEMP_DIR = os.path.join(self.BASE_DIR, 'temp')

        config_path = os.path.join(self.BASE_DIR, 'config.ini')
        self.config = configparser.ConfigParser()

        try:
            with open(config_path, 'r', encoding='utf-8') as fp:
                self.config.read_file(fp)
        except FileNotFoundError:
            raise Exception(f"Config file not found at {config_path}")

        self._load_bot_settings()
        self._load_telegram_settings()
        self._load_parser_settings()

        os.makedirs(self.TEMP_DIR, exist_ok=True)

    def _load_bot_settings(self):
        self.BOT_TOKEN = self.config.get('Bot', 'TOKEN')

        self.LOCALE = self.config.get('Bot', 'LOCALE', fallback='RU').upper()
        if self.LOCALE not in ['RU', 'EN']:
            self.LOCALE = 'RU'

        self.ADMINS = [
            int(admin.strip())
            for admin in self.config.get('Bot', 'ADMINS').split(',')
            if admin.strip()
        ]

    def _load_telegram_settings(self):
        self.API_ID = self.config.getint('Telegram', 'API_ID')
        self.API_HASH = self.config.get('Telegram', 'API_HASH')
        self.PHONE = self.config.get('Telegram', 'PHONE')

    def _load_parser_settings(self):
        self.BATCH_SIZE = self.config.getint('Parser', 'BATCH_SIZE')


config = Config()

BOT_TOKEN = config.BOT_TOKEN
LOCALE = config.LOCALE
ADMINS = config.ADMINS

API_ID = config.API_ID
API_HASH = config.API_HASH
PHONE = config.PHONE

BASE_DIR = config.BASE_DIR
DATA_DIR = config.DATA_DIR
TEMP_DIR = config.TEMP_DIR

BATCH_SIZE = config.BATCH_SIZE
