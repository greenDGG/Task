import asyncio
from playwright.async_api import async_playwright
from youtube.browser import launch_browser
from youtube.cookies import save_cookies

YOUTUBE_URL = "https://www.youtube.com"


async def main():
    print("=== SETUP YOUTUBE - OBTENER COOKIES ===")
    print("Se abrira Chrome. Inicia sesion en YouTube manualmente.")
    print("Cuando termines, cierra la pestana o presiona Ctrl+C")
    print("Las cookies se guardaran automaticamente.\n")

    async with async_playwright() as p:
        browser = await launch_browser(p)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="es-ES",
        )
        page = await context.new_page()
        await page.goto(YOUTUBE_URL, wait_until="networkidle")
        print("Navega a YouTube e inicia sesion. Vuelve a esta terminal cuando termines.")

        input("Presiona Enter cuando hayas iniciado sesion y estes en YouTube...")

        await save_cookies(context)
        print("Cookies guardadas correctamente!")

        await browser.close()
        print("Chrome cerrado. Listo para usar main.py")


if __name__ == "__main__":
    asyncio.run(main())
