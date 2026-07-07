import os, json

COOKIES_DIR = "sessions"
COOKIES_FILE = os.path.join(COOKIES_DIR, "youtube_cookies.json")


async def save_cookies(context):
    os.makedirs(COOKIES_DIR, exist_ok=True)
    cookies = await context.cookies()
    with open(COOKIES_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)
    print(f"[cookies] Guardadas {len(cookies)} cookies en {COOKIES_FILE}")


async def load_cookies(context):
    if not os.path.exists(COOKIES_FILE):
        print("[cookies] No se encontraron cookies guardadas")
        return False
    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    await context.add_cookies(cookies)
    print(f"[cookies] Cargadas {len(cookies)} cookies")
    return True
