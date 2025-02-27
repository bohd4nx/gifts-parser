from data.config import LOCALE
from .formatter import format_number

TEXTS = {
    'RU': {
        'status_message': lambda chat, total, processed, found, percent, eta, batch_info='': (
            f"🔍 <b>Парсинг чата{batch_info}: @{chat}</b>\n\n"
            f"📊 <b>Всего участников:</b> {format_number(total)}\n"
            f"👤 <b>Обработано:</b> {format_number(processed)}/{format_number(total)} ({percent}%)\n"
            f"✨ <b>Найдено пользователей:</b> {format_number(found)}\n\n"
            f"⌛️ <b>Осталось примерно:</b> {eta}"
        ),
        'final_message': lambda chat, total, processed, found, percent, elapsed, stopped: (
            f"⏹ <b>Парсинг чата: @{chat} {'остановлен пользователем' if stopped else 'завершен'}</b>\n\n"
            f"📊 <b>Всего участников:</b> {format_number(total)}\n"
            f"👤 <b>Обработано:</b> {format_number(processed)}/{format_number(total)} ({percent}%)\n"
            f"✨ <b>Найдено пользователей:</b> {format_number(found)}\n\n"
            f"⌛️ <b>Затрачено времени:</b> {elapsed}\n\n"
            f"❗Лимит парса участников - 10к/чат (Уважайте правила Telegram)"
        ),
        'init_text': """
🔄 <b>Инициализация парсинга...</b>

<blockquote expandable><i>Если инициализация занимает больше времени, чем ожидалось, проверьте:</i>

1️⃣ Все зависимости правильно установлены
2️⃣ Вы успешно авторизовались с помощью <b>номера телефона</b>
3️⃣ Проверьте логи консоли на наличие ошибок

❗️ Если проблемы не устраняются, свяжитесь с @bohd4nx</blockquote>

<i>Пожалуйста, подождите, пока устанавливается соединение...</i>
""",
        'start_text': """
<b>👋 Привет, {}</b>

<blockquote expandable><b>ℹ️ Важная информация:</b>
• Я могу парсить только <b>публичные группы</b>
• Группы должны иметь <b>видимый список участников</b>
• Приватные группы и каналы <b>не поддерживаются</b>
• Обработка больших групп может занять некоторое время

<b>📝 Как использовать:</b>
1. Отправьте мне ссылку на публичную группу (например, @groupname или https://t.me/groupname)
2. Дождитесь завершения процесса парсинга
3. Скачайте файл с результатами

<b>⚠️ Ограничения:</b>
• Нельзя парсить приватные группы
• Нельзя парсить группы со скрытыми участниками
• Могут применяться ограничения по частоте запросов</blockquote>

<b>🚀 Все понятно? Отправьте мне ссылку на группу!</b>

<b>Made with ❤️ by @bohd4nx</b>
""",
        'buttons': {
            'stop_parsing': "⛔️ Остановить парсинг",
            'download_results': "📥 Скачать результаты"
        },
        'errors': {
            'nothing_to_stop': "❌ Нечего останавливать",
            'cant_get_members': "❌ Не удалось получить количество участников. Убедитесь, что группа публичная и доступная.",
            'parse_error': "❌ Произошла ошибка: {}",
            'results_not_found': "Результаты не найдены",
            'download_error': "Ошибка при загрузке результатов"
        },
        'batch_info': lambda current, total: f" [{current}/{total}]",
        'error_next': "❌ Ошибка парсинга, переход к следующей ссылке...",
        'final_batch_message': "✅ Обработка всех ссылок завершена!"
    },
    'EN': {
        'status_message': lambda chat, total, processed, found, percent, eta, batch_info='': (
            f"🔍 <b>Parsing chat{batch_info}: @{chat}</b>\n\n"
            f"📊 <b>Total members:</b> {format_number(total)}\n"
            f"👤 <b>Processed:</b> {format_number(processed)}/{format_number(total)} ({percent}%)\n"
            f"✨ <b>Users found:</b> {format_number(found)}\n\n"
            f"⌛️ <b>ETA:</b> {eta}"
        ),
        'final_message': lambda chat, total, processed, found, percent, elapsed, stopped: (
            f"⏹ <b>Parsing chat: @{chat} {'stopped by user' if stopped else 'completed'}</b>\n\n"
            f"📊 <b>Total members:</b> {format_number(total)}\n"
            f"👤 <b>Processed:</b> {format_number(processed)}/{format_number(total)} ({percent}%)\n"
            f"✨ <b>Users found:</b> {format_number(found)}\n\n"
            f"⌛️ <b>Time elapsed:</b> {elapsed}\n\n"
            f"❗Parsing limit - 10k/chat (Please respect Telegram's ToS)"
        ),
        'init_text': """
🔄 <b>Initializing parsing...</b>

<blockquote expandable><i>If initialization takes longer than expected, please check:</i>

1️⃣ All dependencies are properly installed
2️⃣ You have successfully authenticated with your <b>phone number</b>
3️⃣ Check console logs for any errors

❗️ If issues persist, contact @bohd4nx</blockquote>

<i>Please wait while establishing connection...</i>
""",
        'start_text': """
<b>👋 Hello, {}</b>

<blockquote expandable><b>ℹ️ Important information:</b>
• I can only parse <b>public groups</b>
• Groups must have <b>visible member list</b>
• Private groups and channels are <b>not supported</b>
• Processing large groups may take some time

<b>📝 How to use:</b>
1. Send me a public group link (e.g., @groupname or https://t.me/groupname)
2. Wait for the parsing process to complete
3. Download the results file

<b>⚠️ Limitations:</b>
• Cannot parse private groups
• Cannot parse groups with hidden members
• Rate limits may apply</blockquote>

<b>🚀 Ready? Send me a group link!</b>

<b>Made with ❤️ by @bohd4nx</b>
""",
        'buttons': {
            'stop_parsing': "⛔️ Stop Parsing",
            'download_results': "📥 Download Results"
        },
        'errors': {
            'nothing_to_stop': "❌ Nothing to stop",
            'cant_get_members': "❌ Could not get member count. Make sure the group is public and accessible.",
            'parse_error': "❌ An error occurred: {}",
            'results_not_found': "Results not found",
            'download_error': "Error downloading results"
        },
        'batch_info': lambda current, total: f" [{current}/{total}]",
        'error_next': "❌ Parse error, moving to next link...",
        'final_batch_message': "✅ All links processing completed!"
    }
}


def get_status_message(chat: str, total: int, processed: int, found: int, percent: float, eta: str,
                       batch_info: str = '') -> str:
    return TEXTS[LOCALE]['status_message'](chat, total, processed, found, percent, eta, batch_info)


def get_final_message(chat: str, total: int, processed: int, found: int, percent: float, elapsed: str,
                      stopped: bool = False) -> str:
    return TEXTS[LOCALE]['final_message'](chat, total, processed, found, percent, elapsed, stopped)


def get_button_text(key: str) -> str:
    return TEXTS[LOCALE]['buttons'][key]


def get_error_text(key: str, *args) -> str:
    return TEXTS[LOCALE]['errors'][key].format(*args)


def get_batch_info(current: int, total: int) -> str:
    return TEXTS[LOCALE]['batch_info'](current, total)


def get_error_next() -> str:
    return TEXTS[LOCALE]['error_next']


def get_final_batch_message() -> str:
    return TEXTS[LOCALE]['final_batch_message']


INIT_TEXT = TEXTS[LOCALE]['init_text']
START_TEXT = TEXTS[LOCALE]['start_text']
