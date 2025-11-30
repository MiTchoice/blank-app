import time, schedule, threading
from pathlib import Path
import capture, classify, planner, nudge

def job_capture():
    capture.snapshot()

def job_end_of_day():
    day = Path(__file__).resolve().parent.parent / "data" / f"{planner.datetime.date.today().isoformat()}_detected.csv"
    if not day.exists():
        classify.rule_engine(planner.datetime.date.today().isoformat())
    planner.plan()

def job_alarms():
    nudge.run_alarms()

# schedule
schedule.every(2).minutes.do(job_capture)
schedule.every().day.at("23:59").do(job_end_of_day)
schedule.every().hour.do(job_alarms)

# run threaded
def worker():
    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=worker, daemon=True).start()
print("Daily-life coach running…  Ctrl+C to stop.")
while True:
    time.sleep(1)