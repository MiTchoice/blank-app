import json, datetime, os, time, win32api
from pathlib import Path

LOG = Path(__file__).resolve().parent.parent / "data" / "raw_log.jsonl"

def snapshot():
    """Collect trivial signals every 2 min."""
    idle_ms = win32api.GetTickCount() - win32api.GetLastInputInfo()
    idle_min = idle_ms / 1000 / 60
    rec = {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "idle_min": round(idle_min, 1),
        "charging": bool(os.system('powershell "(Get-WmiObject -Class BatteryStatus).Charging" >nul 2>&1')),
        "day": datetime.date.today().isoformat()
    }
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")

if __name__ == "__main__":
    while True:
        snapshot()
        time.sleep(120)