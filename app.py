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
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns(12)
        staff_available_df = staff_data_df[~staff_data_df['STAFF NAME'].isin(df_absent['STAFF NAME'])]
        staff_available_df = staff_available_df.groupby(by=['DEPARTMENT']).count()
        staff_groupby_df = staff_data_df.groupby(by=['DEPARTMENT']).count()

        col1.metric(label="WELDER", value=staff_available_df.loc['WELDER'], delta=int(staff_available_df.loc['WELDER'].values[0]) - int(staff_groupby_df.loc['WELDER'].values[0]))
        col2.metric(label="INTERIOR", value=staff_available_df.loc['INTERIOR'], delta=int(staff_available_df.loc['INTERIOR'].values[0]) - int(staff_groupby_df.loc['INTERIOR'].values[0]))
        col3.metric(label="FRAME", value=staff_available_df.loc['FRAME'], delta=int(staff_available_df.loc['FRAME'].values[0]) - int(staff_groupby_df.loc['FRAME'].values[0]))
        col4.metric(label="FABRIC", value=staff_available_df.loc['FABRIC'], delta=int(staff_available_df.loc['FABRIC'].values[0]) - int(staff_groupby_df.loc['FABRIC'].values[0]))
        col5.metric(label="SEWING", value=staff_available_df.loc['SEWING'], delta=int(staff_available_df.loc['SEWING'].values[0]) - int(staff_groupby_df.loc['SEWING'].values[0]))
        col6.metric(label="SPONGE", value=staff_available_df.loc['SPONGE'], delta=int(staff_available_df.loc['SPONGE'].values[0]) - int(staff_groupby_df.loc['SPONGE'].values[0]))
        col7.metric(label="SPRAY", value=staff_available_df.loc['SPRAY'], delta=int(staff_available_df.loc['SPRAY'].values[0]) - int(staff_groupby_df.loc['SPRAY'].values[0]))
        col8.metric(label="ASSEMBLY", value=staff_available_df.loc['ASSEMBLY'], delta=int(staff_available_df.loc['ASSEMBLY'].values[0]) - int(staff_groupby_df.loc['ASSEMBLY'].values[0]))
        col9.metric(label="PACKING", value=staff_available_df.loc['PACKING'], delta=int(staff_available_df.loc['PACKING'].values[0]) - int(staff_groupby_df.loc['PACKING'].values[0]))
        col10.metric(label="OUTDOOR", value=staff_available_df.loc['OUTDOOR'], delta=int(staff_available_df.loc['OUTDOOR'].values[0]) - int(staff_groupby_df.loc['OUTDOOR'].values[0]))
        col11.metric(label="R&D", value=staff_available_df.loc['R&D'], delta=int(staff_available_df.loc['R&D'].values[0]) - int(staff_groupby_df.loc['R&D'].values[0]))

        st.table(df_absent)

        st.header(f"Gatepass on {sel_date}")
        st.table(df_gatepass)

    else:
        st.header(f"All Leave Data")
        st.dataframe(df)
