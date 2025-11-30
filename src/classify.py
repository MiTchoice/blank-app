import pandas as pd, joblib, datetime, pathlib
MODELS = pathlib.Path(__file__).resolve().parent.parent / "models"
DATA   = pathlib.Path(__file__).resolve().parent.parent / "data"

pipe = joblib.load(MODELS / "rf.pkl")

def rule_engine(day: str):
    df = pd.read_json(DATA / "raw_log.jsonl", lines=True)
    df = df[df.day == day].copy()
    if df.empty:
        pd.DataFrame(columns=["activity","hour"]).to_csv(DATA / f"{day}_detected.csv", index=False)
        return
    preds = pipe.predict(df[["hour", "idle_min", "charging"]])
    df["activity"] = preds
    # keep only real activities
    df = df[df.activity != "none"]
    out = DATA / f"{day}_detected.csv"
    df[["activity","hour"]].to_csv(out, index=False)
    return out