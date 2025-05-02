import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from streamlit_calendar import calendar

## Load data from ALL E LEAVE RECORDS - tabsheet : DATA
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=3000)
df = df.dropna(how="all")

st.title("Staff Absent List :")
# sel_date = st.date_input("pick a date").strftime('%m/%d/%Y')

# show calendar; returns a dict with callbacks (e.g. dateClick)
cal_ret = calendar(key="leave_cal")  

# extract ISO date when user clicks a day
if cal_ret and cal_ret.get("callback") == "dateClick":
    # e.g. "2025-05-29T00:00:00.000Z" → "05/29/2025"
    sel_date = cal_ret["dateClick"]["date"].split("T")[0]
    sel_date = pd.to_datetime(sel_date).strftime('%m/%d/%Y')
    # text = st.write("yahoo")
else:
     # fallback to today
     sel_date = pd.Timestamp("today").strftime('%m/%d/%Y')
    #  text = st.write("naweee")

# cal_ret
sel_date
# text


df['LEAVE ON'] = pd.to_datetime(df["LEAVE ON"]).dt.strftime('%m/%d/%Y')
df['LEAVE UNTIL'] = pd.to_datetime(df["LEAVE UNTIL"]).dt.strftime('%m/%d/%Y')


mask = (df['LEAVE ON'] <= sel_date) & (df['LEAVE UNTIL'] >= sel_date)

df_absent = df.loc[mask, ['STAFF NAME','LEAVE ON','LEAVE UNTIL', 'REASON']]
df_absent = pd.DataFrame.from_dict(df_absent)

@st.dialog("MEH")
def meh():
    df_absent

meh()
