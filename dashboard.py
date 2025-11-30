import pandas as pd, pathlib, datetime, altair as alt, streamlit as st
DATA = pathlib.Path("data")

st.set_page_config(page_title="My-day coach", layout="centered")
st.title("📊 M-Tech First – Life-log dashboard")

# file selector
day = st.sidebar.date_input("Pick day", datetime.date.today())
csv = DATA / f"{day}_detected.csv"
jsonl = DATA / "raw_log.jsonl"

if csv.exists():
    df_act = pd.read_csv(csv)
    st.subheader("Detected activities")
    st.dataframe(df_act)
    c = alt.Chart(df_act).mark_bar().encode(x='activity', y='hour')
    st.altair_chart(c, use_container_width=True)
else:
    st.info("No activities detected for this day yet.")

# raw sensor timeline
if jsonl.exists():
    df_raw = pd.read_json(jsonl, lines=True)
    df_raw['ts'] = pd.to_datetime(df_raw.ts)
    st.subheader("Raw sensor timeline")
    st.line_chart(df_raw.set_index('ts')[['idle_min']])