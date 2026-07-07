import os, time, re, asyncio

SCREENSHOTS_DIR = "screenshots"


def _extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else "unknown"


async def _accept_cookies(page):
    selectores = [
        "button:has-text('Accept all')",
        "button:has-text('Aceptar todo')",
        "button:has-text('Aceptar')",
        "button[aria-label*='Accept']",
        "form button:has-text('Accept')",
        "button:has-text('I agree')",
        "button:has-text('De acuerdo')",
        "#consent-bump button:has-text('Accept')",
    ]
    for sel in selectores:
        try:
            btn = page.locator(sel).first
            if await btn.count() > 0:
                await btn.click(timeout=3000)
                await page.wait_for_timeout(1000)
                print("[actions] Cookies aceptadas")
                return True
        except:
            pass
    return False


async def _click_play(page):
    selectores = [
        ".ytp-large-play-button",
        "button.ytp-large-play-button",
        "button[aria-label*='reproducción']",
        "button[aria-label*='play']",
        "button[aria-label*='Play']",
    ]
    for sel in selectores:
        try:
            btn = page.locator(sel).first
            if await btn.count() > 0:
                await btn.click(timeout=3000)
                print("[actions] Play clickeado")
                await page.wait_for_timeout(2000)
                return True
        except:
            pass
    return False


async def go_to_video(page, url):
    print(f"[actions] Navegando a {url}")
    await page.goto(url, wait_until="commit", timeout=30000)
    await page.wait_for_timeout(4000)
    await _accept_cookies(page)
    await _click_play(page)
    await page.wait_for_timeout(2000)


async def skip_ad(page):
    max_rounds = 5
    for ronda in range(max_rounds):
        try:
            ad_badge = page.locator(".ytp-ad-badge__text--clean-player")
            if await ad_badge.count() == 0 or not await ad_badge.is_visible():
                if ronda == 0:
                    print("[actions] No hay anuncio")
                else:
                    print("[actions] Fin de anuncios")
                return False
        except:
            if ronda == 0:
                print("[actions] No hay anuncio")
            return False

        print(f"[actions] Anuncio detectado (ronda {ronda+1}), esperando boton saltar...")
        selectores = [
            "button.ytp-skip-ad-button",
            "button.ytp-ad-skip-button",
            "button[aria-label*='Skip']",
            "button[aria-label*='Saltar']",
            ".ytp-ad-skip-button-modern",
        ]
        saltado = False
        for _ in range(15):
            for sel in selectores:
                try:
                    btn = page.locator(sel).first
                    if await btn.count() > 0:
                        await btn.click(timeout=2000)
                        print("[actions] Anuncio saltado")
                        await page.wait_for_timeout(1500)
                        saltado = True
                        break
                except:
                    pass
            if saltado:
                break
            await asyncio.sleep(1)

        if not saltado:
            print("[actions] No aparecio boton saltar")
            return False

    print("[actions] Demasiados anuncios seguidos, saliendo")
    return False


async def _esperar_elemento(page, selectores, timeout=10):
    for _ in range(timeout):
        for sel in selectores:
            try:
                btn = page.locator(sel).first
                if await btn.count() > 0:
                    return btn
            except:
                pass
        await asyncio.sleep(1)
    return None


async def click_like(page):
    await page.wait_for_timeout(2000)
    selectores = [
        "button[aria-label*='like i']",
        "button[aria-label*='Like']",
        "button[aria-label*='like']",
        "button[aria-label*='Me gusta']",
        "like-button-view-model button",
    ]
    btn = await _esperar_elemento(page, selectores, timeout=10)
    if not btn:
        print("[actions] No se encontro boton like")
        return False
    try:
        pressed = await btn.get_attribute("aria-pressed")
        if pressed == "true":
            print("[actions] Ya tiene like")
            return False
        await btn.click(timeout=3000)
        print("[actions] Like clickeado")
        return True
    except Exception as e:
        print(f"[actions] Error like: {e}")
        return False


async def click_subscribe(page):
    await page.wait_for_timeout(1000)
    try:
        container = page.locator("ytd-subscribe-button-renderer[subscribed]")
        if await container.count() > 0:
            print("[actions] Ya esta suscrito")
            return False
    except:
        pass

    selectores = [
        "#subscribe-button-shape button",
        "button[aria-label*='Subscribe']",
        "button[aria-label*='Suscribirse']",
        "button[aria-label*='subscribe']",
        "button[aria-label*='suscribir']",
    ]
    btn = await _esperar_elemento(page, selectores, timeout=10)
    if not btn:
        print("[actions] No se encontro boton subscribe")
        return False
    try:
        text = await btn.inner_text()
        if "subscribed" in text.lower() or "suscrito" in text.lower():
            print("[actions] Ya esta suscrito")
            return False
        await btn.click(timeout=3000)
        print("[actions] Subscribe clickeado")
        return True
    except Exception as e:
        print(f"[actions] Error subscribe: {e}")
        return False


async def take_screenshot(page, url):
    await page.wait_for_timeout(3000)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    video_id = _extract_video_id(url)
    filename = f"{video_id}_{int(time.time())}.png"
    path = os.path.join(os.path.abspath(SCREENSHOTS_DIR), filename)
    await page.screenshot(path=path, full_page=False)
    print(f"[actions] Screenshot guardado: {path}")
    return path
