from telethon import TelegramClient, events


SESSION_FILE = "sessions/telegram_session"


class Bot:
    def __init__(self, api_id, api_hash, allowed_chat_id):
        self.api_id = api_id
        self.api_hash = api_hash
        self.allowed_chat_id = allowed_chat_id
        self._resolve_chat_id = None
        self._processed = set()
        self.client = TelegramClient(SESSION_FILE, api_id, api_hash)

    async def send_message(self, chat_id, text):
        await self.client.send_message(chat_id, text)

    async def send_photo(self, chat_id, photo_path, caption=""):
        await self.client.send_file(chat_id, photo_path, caption=caption)

    async def start(self):
        await self.client.start()
        me = await self.client.get_me()
        print(f"[telegram] Sesion iniciada como {me.first_name}")

        if not str(self.allowed_chat_id).lstrip("-").isdigit():
            entity = await self.client.get_entity(self.allowed_chat_id)
            self._resolve_chat_id = entity.id
            print(f"[telegram] Escuchando desde: {self.allowed_chat_id} (id: {entity.id})")
        else:
            self._resolve_chat_id = int(self.allowed_chat_id)
            print(f"[telegram] Escuchando desde chat id: {self._resolve_chat_id}")

    async def stop(self):
        await self.client.disconnect()

    def on_new_message(self, handler):
        @self.client.on(events.NewMessage)
        async def wrapper(event):
            if event.chat_id != self._resolve_chat_id:
                return
            msg_id = f"{event.chat_id}:{event.message.id}"
            if msg_id in self._processed:
                return
            self._processed.add(msg_id)
            await handler(event)
        return wrapper
