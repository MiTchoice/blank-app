from win10toast_click import ToastNotifier
import pandas as pd, datetime, pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
toaster = ToastNotifier()

def show_toast(activity, start, duration):
    advice = {
        "breakfast": "Grab a 5-min oat bowl 🥣",
        "lunch": "Try a 10-min chickpea salad 🥗",
        "dinner": "Keep screen off while eating 🍽",
        "study": "Pomodoro 25-min blocks 📚"
    }
    msg = f"{advice.get(activity,'')}  (suggested {start:02d}:00 for {duration} min)"
    toaster.show_toast(f"Up next: {activity}", msg,
                       duration=10, threaded=True)

def run_alarms():
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    plan_csv = DATA / f"{tomorrow}_plan.csv"
    if not plan_csv.exists():
        return
    df = pd.read_csv(plan_csv)
    now = datetime.datetime.now().hour
    for _, row in df.iterrows():
        if pd.notna(row.alarm) and int(row.alarm) == now:
            show_toast(row.activity, int(row.start), int(row.duration))