import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from streamlit_calendar import calendar

st.set_page_config(layout="wide")

## Load data from ALL E LEAVE RECORDS - tabsheet : DATA
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=3000)
# df = df.dropna(how="all")
df_outfilter_gatepass = df[df['GATEPASS OUT'].isna() | (df['GATEPASS OUT'] == '')]
df_outfilter_gatepass = df_outfilter_gatepass[df_outfilter_gatepass['GATEPASS IN'].isna() | (df_outfilter_gatepass['GATEPASS IN'] == '')]
clean_df = df.drop(['E LEAVE RECORDS', 'GATEPASS OUT', 'GATEPASS IN', 'DIVISION'], axis=1)

staff_data_df = st.connection("staffdata", type=GSheetsConnection).read(worksheet="STAFF DATA", ttl=3000)
staff_data_df = staff_data_df[(staff_data_df['WORK STATUS'] == 'NO STATUS')]
staff_data_df = staff_data_df[['DEPARTMENT', 'STAFF NAME' ]]

st.title("GA E-Leave Calendar 📅")

# Convert date columns
df['LEAVE ON'] = pd.to_datetime(df["LEAVE ON"])
df['LEAVE UNTIL'] = pd.to_datetime(df["LEAVE UNTIL"])

# Generate per-day records for each staff leave
all_dates = []
for _, row in df.iterrows():
    if pd.notna(row['LEAVE ON']) and pd.notna(row['LEAVE UNTIL']):
        leave_range = pd.date_range(start=row['LEAVE ON'], end=row['LEAVE UNTIL'])
        for day in leave_range:
            all_dates.append({'date': day.date(), 'staff': row['STAFF NAME']})

# Count how many staff absent per day
calendar_df = pd.DataFrame(all_dates)
summary = calendar_df.groupby('date').count().reset_index()
summary.columns = ['date', 'count']

# Format for streamlit_calendar
events = [
    {
        "title": f"{row['count']} Absent",
        "start": row['date'].strftime("%Y-%m-%d"),
        "allDay": True,
    }
    for _, row in summary.iterrows()
]

# Show calendar
cal_options = {
    "initialView": "dayGridMonth",
    "headerToolbar": {
        "start": "prev,next today",
        "center": "title",
        "end": "dayGridMonth,timeGridWeek"
    },
    "events": events,
}
col1, col2 = st.columns([1,1.5])

# add session state to store calendar click events
if 'leave_cal' not in st.session_state:
    st.session_state.leave_cal = {}
elif 'eventClick' not in st.session_state.leave_cal:
    st.session_state.leave_cal = {}
elif st.session_state.leave_cal["eventClick"]["event"] != None: 
    st.session_state.leave_cal = st.session_state.leave_cal["eventClick"]["event"]


with col1:
    cal_ret = calendar(key="leave_cal", options=cal_options, events=events)
    with st.expander("Debug"):
        st.session_state.leave_cal

with col2:
    ## extract ISO date when user clicks a day
    if st.session_state.leave_cal != {}:
        ## e.g. "2025-05-29T00:00:00.000Z" → "05/29/2025"
        sel_date = st.session_state.leave_cal
        
        sel_date = pd.to_datetime(sel_date.get('start')).strftime('%m/%d/%Y')
        # text = st.write("yahoo")

        df['LEAVE ON'] = pd.to_datetime(df["LEAVE ON"]).dt.strftime('%m/%d/%Y')
        df['LEAVE UNTIL'] = pd.to_datetime(df["LEAVE UNTIL"]).dt.strftime('%m/%d/%Y')

        mask = (df['LEAVE ON'] <= sel_date) & (df['LEAVE UNTIL'] >= sel_date)

        # df_absent = df.loc[mask, ['TIMESTAMP', 'DEPARTMENT','STAFF NAME','LEAVE ON','LEAVE UNTIL', 'REASON']]
        df_absent = df_outfilter_gatepass.loc[mask, df_outfilter_gatepass.columns]
        df_absent = pd.DataFrame.from_dict(df_absent)
        df_absent = df_absent[['TIMESTAMP', 'DEPARTMENT','STAFF NAME','LEAVE ON','LEAVE UNTIL', 'REASON']]

        df_gatepass = df.loc[mask, df.columns]
        df_gatepass = df_gatepass[~df_gatepass['STAFF NAME'].isin(df_absent['STAFF NAME'])]
        df_gatepass = df_gatepass[['TIMESTAMP', 'DEPARTMENT','STAFF NAME','GATEPASS OUT','GATEPASS IN', 'REASON']]

        # @st.dialog(f"Staff Absent on {sel_date}")
        # def displayListAbsent():
        #     df_absent
        # displayListAbsent()

        st.header(f"Staff Leave on {sel_date}")
        cols = st.columns(12)
        staff_available_df = staff_data_df[~staff_data_df['STAFF NAME'].isin(df_absent['STAFF NAME'])]
        available_count = staff_available_df.groupby(by=['DEPARTMENT']).size() # count available staff per department
        total_count = staff_data_df.groupby(by=['DEPARTMENT']).size() # count total staff per department

        departments = ["WELDER", "INTERIOR", "FRAME", "FABRIC", "SEWING", "SPONGE", "SPRAY", "ASSEMBLY", "PACKING", "OUTDOOR", "R&D"]

        # Display metrics
        for i, dept in enumerate(departments):
            available = int(available_count.get(dept, 0))
            total = int(total_count.get(dept, 0))
            delta = available - total
            cols[i].metric(label=dept, value=available, delta=delta)

        st.table(df_absent)

        st.header(f"Gatepass on {sel_date}")
        st.table(df_gatepass)

    else:
        st.header(f"All Leave Data")
        st.dataframe(df)
