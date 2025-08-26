# 🗓️ MyRoster

A simple, interactive web app for submitting your shift availability for roster cycles.  
Built with [Streamlit](https://streamlit.io/) for Excel Building Management and similar teams.

---

## 🚀 Features

- **Roster Period Calculation:**  
  Automatically computes the next roster cycle based on HR's schedule logic.

- **Interactive Shift Selection:**  
  Select your availability for each day and shift (morning, afternoon, evening) in a spreadsheet-like interface.

- **Weekly Shortcuts:**  
  Quickly fill out entire weeks with one click (e.g., "All mornings", "Clear all").

- **Special Dates Highlighting:**  
  See at a glance which days are "Today", "2nd Sunday", and "4th Monday" in the cycle.

- **CSV Export:**  
  Download your completed availability as a CSV file, ready to send to HR.

- **Submission Preview:**  
  Review your selections and copy a ready-to-send email template.

---

## 🏗️ How to Run

1. **Clone this repository:**
    ```sh
    git clone <repo-url>
    cd roster
    ```

2. **(If using dev container)**  
   Open in VS Code and attach to the dev container.

3. **Install dependencies (if needed):**
    ```sh
    pip install -r requirements.txt
    ```

4. **Start the app:**
    ```sh
    streamlit run app.py
    ```

5. **Open in your browser:**  
   The app will provide a local URL (e.g., http://localhost:8501).

---

## 📝 Usage

- Enter your name (and email if you want a copy).
- Select your available shifts for each day.
- Use the weekly shortcuts for faster entry.
- Click **Preview & Submit Availability** to review and download your CSV.
- Copy the suggested email and send your CSV to HR.

---

## 🛠️ Tech Stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

---

## 📂 Project Structure

```
/workspaces/roster/
│
├── app.py                # Streamlit app entrypoint
├── views/
│   └── rosterView1.py    # Main roster UI logic
├── helpers/
│   └── roster.py         # Roster period/date logic
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🙋‍♂️ Author

Luis Faria  
[https://luisfaria.dev](https://luisfaria.dev)

---

## 📄