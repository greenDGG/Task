import asyncio, os, logging
from dotenv import load_dotenv
from playwright.async_api import async_playwright

from telegram.bot import Bot as TelegramBot
from youtube.browser import launch_browser
from youtube.cookies import load_cookies
from youtube.actions import go_to_video, skip_ad, click_like, click_subscribe, take_screenshot
from parser import extract_task_number, extract_youtube_url
from history import exists as history_exists, add as history_add

logging.basicConfig(
    filename="bot.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
ALLOWED_CHAT = os.getenv("ALLOWED_CHAT_ID", "")
ALERT_TARGET = os.getenv("ALERT_CHANNEL", "")

if not API_ID or not API_HASH:
    print("ERROR: Configura API_ID y API_HASH en .env")
    exit(1)
if not ALLOWED_CHAT:
    print("ERROR: Configura ALLOWED_CHAT_ID en .env")
    exit(1)
if not ALERT_TARGET:
    print("ERROR: Configura ALERT_CHANNEL en .env")
    exit(1)

target = f"@{ALERT_TARGET}" if not ALERT_TARGET.startswith("@") and not ALERT_TARGET.lstrip("-").isdigit() else ALERT_TARGET

bot = TelegramBot(API_ID, API_HASH, ALLOWED_CHAT)


async def handle_youtube(url, task_num):
    print(f"[main] Iniciando tarea #{task_num}")
    try:
        async with async_playwright() as p:
            browser = await launch_browser(p)
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                locale="es-ES",
            )

            ok = await load_cookies(context)
            if not ok:
                print("[main] Sin cookies, abortando")
                await browser.close()
                return

            page = await context.new_page()
            await go_to_video(page, url)
            await skip_ad(page)

            await click_like(page)
            await click_subscribe(page)

            screenshot_path = await take_screenshot(page, url)

            if os.path.exists(screenshot_path):
                print(f"[main] Enviando screenshot a {target}")
                await bot.send_photo(target, screenshot_path, caption=f"T{task_num} completado")

            await browser.close()
            print(f"[main] Tarea #{task_num} finalizada")

    except Exception as e:
        logging.error("Error en tarea %s: %s", task_num, e)
        print(f"[main] ERROR: {e}")


@bot.on_new_message
async def handler(event):
    text = event.message.text.strip()
    url = extract_youtube_url(text)
    if not url:
        return
    msg_ts = int(event.message.date.timestamp())
    task_num = extract_task_number(text) or 0
    if history_exists(msg_ts, task_num, url):
        print(f"[main] Tarea #{task_num} ya registrada (ts={msg_ts}), ignorando")
        return
    history_add(msg_ts, task_num, url)
    await handle_youtube(url, task_num)


async def main():
    await bot.start()
    print("Esperando mensajes...")
    await bot.client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
