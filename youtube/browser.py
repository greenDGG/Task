import os


def _headless():
    return os.getenv("HEADLESS", "false").lower() == "true"

# windows chrome // linux chromium
async def launch_browser(p):
    browser = await p.chromium.launch(
        channel="chromium",
        headless=_headless(),
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
        ],
    )
    return browser
