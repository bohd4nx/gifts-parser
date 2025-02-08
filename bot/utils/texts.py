from .formatter import format_number


def get_status_message(chat: str, total: int, processed: int, found: int, percent: float, eta: str) -> str:
    return (
        f"🔍 <b>Парсинг чата: @{chat}</b>\n\n"
        f"📊 <b>Всего участников:</b> {format_number(total)}\n"
        f"⏳ <b>Обработано:</b> {format_number(processed)}/{format_number(total)} ({percent}%)\n"
        f"✨ <b>Найдено пользователей:</b> {format_number(found)}\n\n"
        f"⌛️ <b>Осталось примерно:</b> {eta}"
    )


def get_final_message(chat: str, total: int, processed: int, found: int,
                      percent: float, elapsed: str, stopped: bool = False) -> str:
    status = 'остановлен пользователем' if stopped else 'завершен'
    return (
        f"⏹ <b>Парсинг чата: @{chat} {status}</b>\n\n"
        f"📊 <b>Всего участников:</b> {format_number(total)}\n"
        f"⏳ <b>Обработано:</b> {format_number(processed)}/{format_number(total)} ({percent}%)\n"
        f"✨ <b>Найдено пользователей:</b> {format_number(found)}\n\n"
        f"⌛️ <b>Затрачено времени:</b> {elapsed}\n\n"
        f"❗Лимит парса участников - 10к/чат (Уважайте правила Telegram)"
    )


INIT_TEXT = """
🔄 <b>Инициализация парсинга...</b>

<blockquote expandable><i>Если инициализация занимает больше времени, чем ожидалось, проверьте:</i>

1️⃣ Все зависимости правильно установлены
2️⃣ Вы успешно авторизовались с помощью <b>номера телефона</b>
3️⃣ Проверьте логи консоли на наличие ошибок

❗️ Если проблемы не устраняются, свяжитесь с @B7XX7B</blockquote>

<i>Пожалуйста, подождите, пока устанавливается соединение...</i>
"""

START_TEXT = """
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

<b>Made with ❤️ by @B7XX7B</b>
"""
