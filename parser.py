import re

EMOJI_DIGIT = re.compile(
    r"(?:"
    r"[0-9]\ufe0f\u20e3"
    r"|\U0001f51f"
    r")+"
)

EMOJI_MAP = {
    "0\ufe0f\u20e3": 0,
    "1\ufe0f\u20e3": 1,
    "2\ufe0f\u20e3": 2,
    "3\ufe0f\u20e3": 3,
    "4\ufe0f\u20e3": 4,
    "5\ufe0f\u20e3": 5,
    "6\ufe0f\u20e3": 6,
    "7\ufe0f\u20e3": 7,
    "8\ufe0f\u20e3": 8,
    "9\ufe0f\u20e3": 9,
    "\U0001f51f": 10,
}

YOUTUBE_RE = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}"
)


def _parse_emoji_number(s):
    num = 0
    i = 0
    while i < len(s):
        if s[i] == "\U0001f51f":
            num = num * 100 + 10 if num > 0 else 10
            i += 1
        else:
            d = int(s[i])
            num = num * 10 + d
            i += 3
    return num


def extract_task_number(text):
    match = EMOJI_DIGIT.search(text)
    if not match:
        return None
    return _parse_emoji_number(match.group())


def extract_youtube_url(text):
    match = YOUTUBE_RE.search(text)
    if match:
        return match.group()
    return None
