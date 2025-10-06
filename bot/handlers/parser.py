import logging
import time
from datetime import datetime

from aiogram.types import Message, BufferedInputFile
from aiogram_i18n import I18nContext
from pyrogram import Client

from bot.methods import get_regular_members, get_large_members
from bot.utils import create_file_content, format_number, format_time, is_large_chat, fetch_gifts_list

logger = logging.getLogger(__name__)


async def process_chat_parsing(
        client: Client,
        message: Message,
        i18n: I18nContext,
        chat_username: str,
        member_count: int,
        progress_message: Message
) -> None:
    gift_mappings = await fetch_gifts_list()
    logger.info(f"Starting parse for {chat_username}, loaded {len(gift_mappings)} gift mappings")

    parser = get_large_members if is_large_chat(member_count) else get_regular_members
    logger.info(f"Chat {chat_username} has {member_count} members, using appropriate parser")

    user_gifts_dict = {}
    total_processed = 0
    start_time = time.time()

    try:
        async for result in parser(client, chat_username, gift_mappings):
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

            update_interval = 300 if is_large_chat(member_count) else 500
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
        logger.error(f"Error during parsing {chat_username}: {e}")
        await progress_message.edit_text(f"Error: {str(e)}")


async def update_progress_message(message, i18n, chat_username, processed, total, found_count, time_value):
    await message.edit_text(
        i18n.get('parsing-progress',
                 chat=chat_username,
                 parsed=format_number(processed),
                 total=format_number(total),
                 found=format_number(found_count),
                 elapsed=format_time(i18n, time_value))
    )
