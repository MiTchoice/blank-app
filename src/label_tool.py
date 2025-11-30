import pandas as pd, json, datetime, pathlib, os, sys
DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
jsonl = DATA / "raw_log.jsonl"
out_csv = DATA / "labelled.csv"

# read what exists
df = pd.read_json(jsonl, lines=True)
df["hour"] = pd.to_datetime(df.ts).dt.hour

# quick console labeller
labels = []
for _, row in df.iterrows():
    os.system('cls')                       # clear screen
    print("Time :", row.ts)
    print("Idle :", row.idle_min, "min")
    print("Hour :", row.hour)
    print("\nActivities: 1 breakfast  2 lunch  3 dinner  4 study  5 job  6 housekeeping  7 sleep  0 none")
    code = input("→ ")
    act_map = {"1":"breakfast","2":"lunch","3":"dinner",
               "4":"study","5":"job","6":"housekeeping","7":"sleep","0":"none"}
    labels.append(act_map.get(code, "none"))
df["activity"] = labels
df.to_csv(out_csv, index=False)
print("saved →", out_csv)