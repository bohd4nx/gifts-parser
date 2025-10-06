import configparser
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    def __init__(self):
        self._load_config()

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / 'config.ini'
        
        if not config_path.exists():
            logger.error(f"Config file not found at {config_path}")
            sys.exit(1)

        config = configparser.ConfigParser()
        config.read(config_path, encoding='utf-8')

        try:
            self.BOT_TOKEN = self._get_required_config(config, 'Bot', 'TOKEN')
            self.LOCALE = config.get('Bot', 'LOCALE', fallback='EN').upper()
            
            self.API_ID = int(self._get_required_config(config, 'Telegram', 'API_ID'))
            self.API_HASH = self._get_required_config(config, 'Telegram', 'API_HASH')
            self.PHONE_NUMBER = config.get('Telegram', 'PHONE_NUMBER', fallback='')
            
        except (ValueError, configparser.Error) as e:
            logger.error(f"Config parsing error: {e}")
            sys.exit(1)

    @staticmethod
    def _get_required_config(config, section, key):
        try:
            value = config.get(section, key).strip()
            if not value:
                raise ValueError(f"Empty value for {section}.{key}")
            return value
        except configparser.NoOptionError:
            logger.error(f"Missing required config: {section}.{key}")
            sys.exit(1)


config = Config()
