import streamlit as st
import pandas as pd
from datetime import timedelta

# ---- ROSTER PERIOD ----
from helpers.roster import start_date, end_date, shifts, dates

def display():
    st.title("🗓️ My Roster")
    st.text("Excel's BM App for your Availability Submission")

    # ---- EMPLOYEE NAME ----
    name = st.text_input("Please enter your name:")

    availability_data = []

    if name:
        st.markdown(
            f"### Hello, **{name}**! \n"
            f"Select the shifts you’re available for each day below:\n"
        )

        # Split dates into weeks
        weeks = []
        current_week = []
        week_start = dates[0]

        for date in dates:
            if date.weekday() == 0 and current_week:
                weeks.append(current_week)
                current_week = []
            current_week.append(date)

        if current_week:
            weeks.append(current_week)

        # Create UI for each week
        for week_num, week_dates in enumerate(weeks, start=1):
            with st.expander(f"📅 Week {week_num}: {week_dates[0].strftime('%d %b')} - {week_dates[-1].strftime('%d %b')}"):
                
                cols = st.columns(len(week_dates))

                for i, date in enumerate(week_dates):
                    with cols[i]:
                        st.write(f"Day **{date.strftime('%a %d %b')}**")
                        selected_shifts = st.multiselect(
                            "Available shifts:",
                            options=shifts,
                            default=[],
                            key=f"{date}",
                            help="Select the shifts you are available for on this day. It can be multiple or none."
                        )
                        for shift in shifts:
                            availability_data.append({
                                "Name": name,
                                "Date": date.strftime("%Y-%m-%d"),
                                "Day": date.strftime("%A"),
                                "Shift": shift,
                                "Available": "YES" if shift in selected_shifts else "NO"
                            })

        # ---- PREVIEW & SUBMIT ----
        if st.button("✅ Preview & Submit Availability"):
            df = pd.DataFrame(availability_data)

            st.success("Here's a preview of your availability:")
            st.dataframe(df)

            # Save locally for testing
            df.to_csv(f"{name}_availability.csv", index=False)

            # Open save dialog for the user
            st.download_button(
                label="Download Availability CSV file",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"{name}_availability.csv",
                mime='text/csv'
            )

            st.success("Your availability has been saved!")

    else:
        st.info("👤 Please enter your name to start.")
