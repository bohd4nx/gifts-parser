from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any


def format_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_users = len(results)
    total_gifts = sum(len(user['gifts']) for user in results)

    gift_stats = defaultdict(int)
    for user in results:
        for gift in user['gifts']:
            gift_stats[gift['name']] += gift['count']

    return {
        'total_users': total_users,
        'total_gifts': total_gifts,
        'gift_stats': dict(gift_stats)
    }


def create_file_content(results: List[Dict[str, Any]], chat_username: str) -> str:
    content = f"Parsed {chat_username} by @bohd4nx's parser on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    user_gifts = defaultdict(list)
    for user in results:
        user_gifts[user['user_id']].extend(user['gifts'])

    for user_id, gifts in user_gifts.items():
        username = gifts[0].get('username', '') if gifts else ''
        
        gift_counts = defaultdict(int)
        for gift in gifts:
            gift_counts[gift['gift_name']] += 1

        gifts_text = ' | '.join(f"{name} x {count}" for name, count in gift_counts.items())
        
        user_prefix = f"@{username} " if username else ""
        content += f"{user_prefix}[{user_id}]: {gifts_text}\n\n"

    return content
