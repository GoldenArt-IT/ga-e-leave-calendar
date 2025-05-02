import streamlit as st
import pandas as pd
from streamlit_calendar import calendar



# --- Sample Delivery Data ---
sample_data = [
    {"Date": "2025-03-01", "Limit Order": "ORD123", "M3": 20, "Deliverer": "Alice", "Lorry": "Truck-7"},
    {"Date": "2025-03-01", "Limit Order": "ORD124", "M3": 20, "Deliverer": "Atan", "Lorry": "Truck-2"},
    {"Date": "2025-03-01", "Limit Order": "ORD125", "M3": 20, "Deliverer": "Atan", "Lorry": "Truck-10"},
    {"Date": "2025-03-05", "Limit Order": "ORD456", "M3": 15, "Deliverer": "Bob", "Lorry": "Truck-3"},
    {"Date": "2025-03-10", "Limit Order": "ORD789", "M3": 25, "Deliverer": "Charlie", "Lorry": "Truck-9"},
    {"Date": "2025-03-15", "Limit Order": "ORD101", "M3": 30, "Deliverer": "David", "Lorry": "Truck-5"},
    {"Date": "2025-03-20", "Limit Order": "ORD102", "M3": 10, "Deliverer": "Emma", "Lorry": "Truck-1"},
]

# Convert to DataFrame
df = pd.DataFrame(sample_data)
df["Date"] = pd.to_datetime(df["Date"])  # Ensure Date is datetime format

# --- Streamlit UI ---
st.title("📅 Delivery Calendar with Pop-Up Dialog")

# Prepare events for calendar
events = []
for _, row in df.iterrows():
    events.append({
        "title": f"Order {row['Limit Order']} ({row['M3']}m³) - {row['Deliverer']} [{row['Lorry']}]",
        "start": row["Date"].strftime("%Y-%m-%d"),  # Convert Timestamp to string
        "metadata": {key: str(value) for key, value in row.items()}   # Convert all values to string
    })

# Calendar options
cal_options = {
    "initialView": "dayGridMonth",
    "headerToolbar": {"start": "prev,next today", "center": "title", "end": "dayGridMonth,timeGridWeek"},
    "editable": False  # Prevent direct editing of events
}

# Display calendar and detect selected event
selected_event = calendar(events=events, options=cal_options, key="calendar")
selected_event

# Show selected event details
# if selected_event:
#     st.write("### Selected Event Details:")
#     st.json(selected_event)
#     st.write(json.dumps(selected_event["eventClick"]["event"]["extendedProps"]["metadata"]))


# --- Pop-up Dialog ---
if selected_event:
    event_metadata = selected_event["eventClick"]["event"]["extendedProps"]["metadata"]
    # st.json(event_metadata)

    @st.dialog(f"📦 Order {event_metadata.get('Limit Order', 'N/A')}")
    def show_event_details():
        st.write(f"📅 **Date:** {event_metadata.get('Date', 'N/A')}")
        st.write(f"📦 **Limit Order:** {event_metadata.get('Limit Order', 'N/A')}")
        st.write(f"📏 **M3 (Cubic Meters):** {event_metadata.get('M3', 'N/A')}")
        st.write(f"🚚 **Deliverer:** {event_metadata.get('Deliverer', 'N/A')}")
        st.write(f"🚛 **Lorry:** {event_metadata.get('Lorry', 'N/A')}")
        if st.button("Close"):
            st.rerun()

    # Trigger the dialog
    show_event_details()
