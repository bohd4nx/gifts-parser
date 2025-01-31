import os
from collections import defaultdict
from typing import Dict, Any

from data.config import TEMP_DIR
from ..core.abstract import BaseDataHandler


class FileService(BaseDataHandler):
    def __init__(self):
        self.base_path = TEMP_DIR

    def get_unique_filename(self, chat: str) -> str:
        base_filename = f'{chat}.txt'
        counter = 1
        filename = os.path.join(self.base_path, base_filename)

        while os.path.exists(filename):
            base_filename = f'{chat}({counter}).txt'
            filename = os.path.join(self.base_path, base_filename)
            counter += 1

        return filename

    def process(self, filepath: str, user_data: list[Dict[str, Any]], username: str, user_id: int) -> None:
        os.makedirs(self.base_path, exist_ok=True)

        gift_counts = defaultdict(int)
        gift_names = {}
        for gift in user_data:
            gift_id = gift['gift']
            gift_counts[gift_id] += 1
            gift_names[gift_id] = gift['gift_name']

        gifts_text = ' | '.join(f"{gift_names[gift_id]} [{gift_id}]: {count}"
                                for gift_id, count in gift_counts.items())

        line = f"@{username} [{user_id}]\n  └─ {gifts_text}\n\n"

        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(line)
