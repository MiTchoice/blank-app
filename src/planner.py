import pandas as pd, datetime
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
TEMPLATE = {
    "breakfast": (7, 15),
    "lunch": (12, 30),
    "dinner": (19, 45),
    "study": (10, 120),
}

def missed_today():
    day = datetime.date.today().isoformat()
    df = pd.read_csv(DATA / f"{day}_detected.csv")
    done = set(df.activity)
    full = set(TEMPLATE.keys())
    return full - done

def plan():
    missed = missed_today()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    plan_csv = DATA / f"{tomorrow}_plan.csv"
    rows = []
    for act, (start, dur) in TEMPLATE.items():
        rows.append({"activity": act, "start": start, "duration": dur,
                     "alarm": start-1 if act in missed else None})
    pd.DataFrame(rows).to_csv(plan_csv, index=False)
    return plan_csv, missed