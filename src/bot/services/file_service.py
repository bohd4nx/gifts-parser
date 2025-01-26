import os
from collections import defaultdict
from typing import Dict, Any

from data.config import TEMP_DIR
from ..core.abstract import BaseDataHandler


class FileService(BaseDataHandler):
    def __init__(self):
        self.base_path = TEMP_DIR

    def process(self, chat: str, user_data: list[Dict[str, Any]], username: str, user_id: int) -> None:
        os.makedirs(self.base_path, exist_ok=True)
        filename = os.path.join(self.base_path, f'{chat}.txt')

        gift_counts = defaultdict(int)
        gift_names = {}
        for gift in user_data:
            gift_id = gift['gift']
            gift_counts[gift_id] += 1
            gift_names[gift_id] = gift['gift_name']

        gifts_text = ' | '.join(f"{gift_names[gift_id]} [{gift_id}]: {count}"
                                for gift_id, count in gift_counts.items())

        line = f"@{username} [{user_id}]\n  └─ {gifts_text}\n\n"

        with open(filename, 'a', encoding='utf-8') as f:
            f.write(line)

    def get_results_path(self, chat: str) -> str:
        return os.path.join(self.base_path, f'{chat}.txt')
