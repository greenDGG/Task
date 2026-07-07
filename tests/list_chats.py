import asyncio, os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")


async def main():
    client = TelegramClient("sessions/telegram_session", API_ID, API_HASH)
    await client.start()
    me = await client.get_me()
    print(f"Sesion: {me.first_name}\n")

    dialogs = await client.get_dialogs()
    print(f"{'ID':<20} {'TIPO':<10} {'NOMBRE'}")
    print("-" * 60)
    for d in dialogs:
        tipo = type(d.entity).__name__.replace("Channel", "Canal").replace("Chat", "Grupo").replace("User", "Usuario")
        print(f"{d.id:<20} {tipo:<10} {d.name or 'sin nombre'}")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
