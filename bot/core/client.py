import os
from typing import Optional

from pyrogram import Client

from data.config import API_HASH, API_ID, DATA_DIR
from .abstract import BaseManager


class ClientManager(BaseManager):
    def __init__(self):
        self.clients = []
        self.session_dir = DATA_DIR

    async def get_client(self) -> Optional[Client]:
        if self.clients:
            client = self.clients[0]
            if client.is_connected:
                return client
            await client.stop()
            self.clients.pop(0)

        session_files = [f for f in os.listdir(self.session_dir) if f.endswith('.session')]
        session_name = 'main' if not session_files else session_files[0].replace('.session', '')

        client = Client(
            name=os.path.join(self.session_dir, session_name),
            api_id=API_ID,
            api_hash=API_HASH
        )

        await client.start()
        self.clients.append(client)
        return client

    async def initialize(self):
        return await self.get_client()

    async def cleanup(self):
        for client in self.clients:
            await client.stop()
        self.clients.clear()
