import streamlit as st
import pandas as pd
from streamlit_calendar import calendar

# st.set_page_config(layout="wide")

# --- Sample Delivery Data ---
sample_data = [
    {"Date": "2025-03-01", "Limit Order": "ORD123", "M3": 20, "Deliverer": "Alice", "Lorry": "Truck-7"},
    {"Date": "2025-03-05", "Limit Order": "ORD456", "M3": 15, "Deliverer": "Bob", "Lorry": "Truck-3"},
    {"Date": "2025-03-10", "Limit Order": "ORD789", "M3": 25, "Deliverer": "Charlie", "Lorry": "Truck-9"},
    {"Date": "2025-03-15", "Limit Order": "ORD101", "M3": 30, "Deliverer": "David", "Lorry": "Truck-5"},
    {"Date": "2025-03-20", "Limit Order": "ORD102", "M3": 10, "Deliverer": "Emma", "Lorry": "Truck-1"},
]

# Convert to DataFrame
df = pd.DataFrame(sample_data)
df["Date"] = pd.to_datetime(df["Date"])

# --- Streamlit UI ---
st.title("📅 Delivery Calendar Demo")

# Prepare events for calendar
events = []
for _, row in df.iterrows():
    events.append({
        "title": f"Order {row['Limit Order']} ({row['M3']}m³) - {row['Deliverer']} [{row['Lorry']}]",
        "start": row["Date"].strftime("%Y-%m-%d")
    })

# Calendar options
cal_options = {
    "initialView": "dayGridMonth",
    "headerToolbar": { "start": "prev,next today", "center": "title", "end": "dayGridMonth,timeGridWeek" }
}

# Display calendar
selected_event = calendar(events=events, options=cal_options, key="calendar")

# Show selected event details
if selected_event:
    st.write("### Selected Event Details:")
    st.json(selected_event)
