import time
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram_i18n import I18nContext

from bot.services import parse_chat
from bot.utils import create_file_content, validate_chat, parse_chat_link, format_number

router = Router(name=__name__)


def create_handler(client):
    @router.message(F.text.regexp(r'@\w+|https?://t\.me/\w+'))
    async def handle_link(message: Message, i18n: I18nContext):
        chat_username = parse_chat_link(message.text)

        is_valid, error_msg, member_count = await validate_chat(message.bot, chat_username, i18n)
        if not is_valid:
            await message.reply(error_msg)
            return

        is_large_chat = member_count > 11000
        progress_key = 'parsing-started-large' if is_large_chat else 'parsing-started'
        progress_message = await message.reply(
            i18n.get(progress_key, chat=chat_username, total=format_number(member_count)))

        user_gifts_dict = {}
        total_processed = 0
        start_time = time.time()

        try:
            async for result in parse_chat(client, chat_username):
                for gift_data in result['gifts']:
                    user_id = gift_data['user_id']
                    if user_id not in user_gifts_dict:
                        user_gifts_dict[user_id] = {
                            'username': gift_data['username'],
                            'user_id': user_id,
                            'gifts': []
                        }
                    user_gifts_dict[user_id]['gifts'].append(gift_data)

                total_processed = result['total_processed']

                update_interval = 300 if is_large_chat else 500
                if total_processed % update_interval == 0:
                    elapsed = time.time() - start_time
                    rate = total_processed / elapsed if elapsed > 0 else 0
                    remaining = member_count - total_processed
                    time_value = remaining / rate if rate > 0 else 0

                    await update_progress_message(
                        progress_message,
                        i18n,
                        chat_username,
                        total_processed,
                        member_count,
                        len(user_gifts_dict),
                        time_value
                    )

            elapsed_total = time.time() - start_time

            if not user_gifts_dict:
                await progress_message.edit_text(i18n.get('no-results', chat=chat_username))
            else:
                results = list(user_gifts_dict.values())
                file_content = create_file_content(results, chat_username)
                file_buffer = BufferedInputFile(
                    file_content.encode('utf-8'),
                    filename=f"{chat_username}_[{message.from_user.id}]_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )

                await message.reply_document(
                    file_buffer,
                    caption=i18n.get('parsing-complete',
                                     chat=chat_username,
                                     total=format_number(member_count),
                                     total_found=format_number(len(results)),
                                     total_parsed=format_number(total_processed),
                                     elapsed=format_time(i18n, elapsed_total))
                )
                await progress_message.delete()
        except Exception as e:
            await progress_message.edit_text(f"Error: {str(e)}")

    return handle_link


async def update_progress_message(message, i18n, chat_username, processed, total, found_count, time_value):
    await message.edit_text(
        i18n.get('parsing-progress',
                 chat=chat_username,
                 parsed=format_number(processed),
                 total=format_number(total),
                 found=format_number(found_count),
                 elapsed=format_time(i18n, time_value))
    )


def format_time(i18n, seconds):
    is_hours = seconds >= 3600
    time_format_key = 'time-format-hours' if is_hours else 'time-format'

    if is_hours:
        time_params = {
            'hours': int(seconds // 3600),
            'minutes': int((seconds % 3600) // 60),
            'seconds': int(seconds % 60)
        }
    else:
        time_params = {
            'minutes': int(seconds // 60),
            'seconds': int(seconds % 60)
        }

    return i18n.get(time_format_key, **time_params)
