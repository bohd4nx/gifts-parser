from bot.i18n import i18n
from data.config import LOCALE
from .helper import format_number

i18n.set_locale(LOCALE.lower())


def get_status_message(chat, total, processed, found, percent, eta, batch_info=''):
    return i18n.get("status_message",
                    chat=chat,
                    total=format_number(total),
                    total_raw=format_number(total),
                    processed=format_number(processed),
                    found=format_number(found),
                    percent=percent,
                    eta=eta,
                    batch_info=batch_info)


def get_final_message(chat, total, processed, found, percent, elapsed, stopped=False):
    status = i18n.get("status.stopped" if stopped else "status.completed")
    return i18n.get("final_message",
                    chat=chat,
                    total=format_number(total),
                    total_raw=format_number(total),
                    processed=format_number(processed),
                    found=format_number(found),
                    percent=percent,
                    elapsed=elapsed,
                    status=status)


def get_button_text(key):
    return i18n.get(f"buttons.{key}")


def get_error_text(key, *args):
    return i18n.get(f"errors.{key}", error=args[0] if args else None)


def get_batch_info(current, total):
    return i18n.get("batch_info", current=current, total=total)


def get_error_next():
    return i18n.get("error_next")


def get_final_batch_message():
    return i18n.get("final_batch_message")


def get_parsing_stopped():
    return i18n.get("parsing_stopped")


INIT_TEXT = i18n.get("init_text")
START_TEXT = i18n.get("start_text")
