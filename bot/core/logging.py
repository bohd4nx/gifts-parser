import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] - %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    logging.getLogger('pyrogram').setLevel(logging.ERROR)
    logging.getLogger('bot.services.parsing').setLevel(logging.DEBUG)
    
    logging.getLogger('aiogram.dispatcher').setLevel(logging.INFO)
    logging.getLogger('aiogram.event').setLevel(logging.ERROR)


logger = logging.getLogger(__name__)
