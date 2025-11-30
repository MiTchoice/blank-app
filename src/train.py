import pandas as pd, joblib, pathlib
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
MODELS = pathlib.Path(__file__).resolve().parent.parent / "models"

df = pd.read_csv(DATA / "labelled.csv")
X = df[["hour", "idle_min", "charging"]]
y = df["activity"]

pre = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(handle_unknown="ignore"), ["charging"])],
    remainder="passthrough"
)
clf = RandomForestClassifier(n_estimators=300, max_depth=None, random_state=42)
pipe = Pipeline(steps=[("prep", pre), ("clf", clf)])
pipe.fit(X, y)

joblib.dump(pipe, MODELS / "rf.pkl")
print("model saved →", MODELS / "rf.pkl")