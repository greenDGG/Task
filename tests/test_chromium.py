import asyncio
from playwright.async_api import async_playwright
from youtube.cookies import load_cookies

YOUTUBE_URL = "https://www.youtube.com"


async def main():
    print("=== TEST COOKIES CON CHROMIUM ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="es-ES",
        )
        ok = await load_cookies(context)
        if not ok:
            print("No hay cookies guardadas. Ejecuta setup_youtube.py primero")
            await browser.close()
            return

        page = await context.new_page()
        await page.goto(YOUTUBE_URL, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)

        print("Ve si aparece tu avatar/logeado. Si ves la pantalla de inicio sin login, las cookies no sirven.")
        input("Presiona Enter para cerrar...")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
