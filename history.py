import os, json

HISTORY_FILE = "historial.json"


def _load():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def exists(ts, task_num, url):
    data = _load()
    for entry in data:
        if entry["timestamp"] == ts and entry["task"] == task_num and entry["url"] == url:
            return True
    return False


def add(ts, task_num, url):
    data = _load()
    data.append({
        "timestamp": ts,
        "task": task_num,
        "url": url,
    })
    _save(data)
