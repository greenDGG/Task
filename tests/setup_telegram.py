import asyncio, os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

SESSION_FILE = "sessions/telegram_session"


async def main():
    print("=== SETUP TELEGRAM - INICIAR SESION ===")
    print("Te pedira tu numero de telefono y codigo de verificacion.\n")

    os.makedirs("sessions", exist_ok=True)
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start()
    me = await client.get_me()
    print(f"\nSesion iniciada como: {me.first_name} (@{me.username}, id: {me.id})")
    print(f"Sesion guardada en {SESSION_FILE}.session")
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
