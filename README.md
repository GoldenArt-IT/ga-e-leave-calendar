# 📅 GA E-Leave Calendar

A **Streamlit** app to visualize leave records on a calendar, track absences per day, and display staff availability by department. Integrates live data from **Google Sheets**.

---

✅ **Access the App:**  
[👉 **GA E-Leave Calendar**](https://ga-e-leave-calendar.streamlit.app/)

---

## 📑 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example Workflow](#example-workflow)
- [Project Structure](#project-structure)
- [Reference](#reference)

---

## ✨ Features

- Google Sheets integration for leave and staff data
- Interactive calendar view showing daily leave counts
- Click a date to see:
  - Staff on leave
  - Staff with gatepass
  - Available staff per department
- Department-wise availability metrics
- Real-time updates on click events

---

## ⚙️ Installation

1. **Clone the repository**

   ```
   git clone https://github.com/your-org/ga-e-leave-calendar.git
   cd ga-e-leave-calendar
   ```

2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:

   ```
   streamlit
   streamlit_gsheets
   pandas
   streamlit-calendar
   ```

3. **Create `secrets.toml`**

   ```toml
   [connections.gsheets]
   email = "your_service_account_email"
   private_key = "-----BEGIN PRIVATE KEY-----\n..."

   [connections.staffdata]
   email = "your_service_account_email"
   private_key = "-----BEGIN PRIVATE KEY-----\n..."

   [allowed_users]
   emails = ["user1@example.com", "user2@example.com"]
   ```

4. **Run the app**

   ```
   streamlit run app.py
   ```

---

## ⚙️ Configuration

- **Google Sheets**
  - First connection (`gsheets`) must contain a worksheet named `DATA` with columns:
    - STAFF NAME
    - LEAVE ON
    - LEAVE UNTIL
    - GATEPASS OUT
    - GATEPASS IN
    - DEPARTMENT
    - REASON
    - TIMESTAMP
  - Second connection (`staffdata`) must have a worksheet `STAFF DATA` with:
    - STAFF NAME
    - DEPARTMENT
    - WORK STATUS

- **Departments Displayed**
  - WELDER
  - INTERIOR
  - FRAME
  - FABRIC
  - SEWING
  - SPONGE
  - SPRAY
  - ASSEMBLY
  - PACKING
  - OUTDOOR
  - R&D

---

## 🛠️ Usage

1. **Load the App**
   - Sidebar shows the calendar with per-day leave counts.

2. **Click a Date**
   - View:
     - Staff on leave (filtered without gatepass)
     - Staff on gatepass
     - Department-wise availability metrics

3. **View All Data**
   - If no date is selected, the app displays all leave records.

---

## 💡 Example Workflow

**Scenario:**

- Staff John Doe applied leave:
  - From: 2025-05-27
  - To: 2025-05-29
- On the calendar:
  - Each date shows `1 Leave`.
- Click **May 28**:
  - John Doe appears under "Staff Leave".
  - Departments show counts of available staff.

**Daily Habit Example:**

- Supervisors open the calendar each morning.
- Click today's date to see who is on leave or gatepass.
- Use metrics to plan daily manpower allocation.

---

## 📂 Project Structure

```
ga-e-leave-calendar/
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
└── README.md           # This README
```

---

## 📚 Reference

- [Streamlit Documentation](https://docs.streamlit.io)
- [streamlit_gsheets](https://github.com/streamlit/streamlit-gsheets)
- [streamlit-calendar](https://github.com/streamlit/streamlit-calendar)
- [Google Sheets API](https://developers.google.com/sheets/api)

---
