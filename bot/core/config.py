import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self):
        self._load_config()

    def _load_config(self):
        env_path = Path(__file__).parent.parent.parent / '.env'

        if not env_path.exists():
            logger.error(f"Environment file not found at {env_path}")
            sys.exit(1)

        load_dotenv(dotenv_path=env_path)

        try:
            self.BOT_TOKEN = self._get_required_env('BOT_TOKEN')
            
            self.API_ID = int(self._get_required_env('API_ID'))
            self.API_HASH = self._get_required_env('API_HASH')
            self.PHONE_NUMBER = os.getenv('PHONE_NUMBER', '')

        except ValueError as e:
            logger.error(f"Config parsing error: {e}")
            sys.exit(1)

    @staticmethod
    def _get_required_env(key):
        value = os.getenv(key)
        if not value:
            logger.error(f"Missing required environment variable: {key}")
            sys.exit(1)
        return value


config = Config()
