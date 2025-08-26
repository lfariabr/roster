import pandas as pd

today = pd.Timestamp.today().normalize()

# Find the next Monday (0 = Monday). If today is Monday, this returns today.
days_until_monday = (0 - today.weekday()) % 7
next_monday = today + pd.Timedelta(days=days_until_monday)

# Start = Monday exactly 2 weeks from now
start_date = next_monday + pd.Timedelta(weeks=3)

# End = last day of a 4-week window (i.e., 28 days total, end on Sunday)
end_date = start_date + pd.Timedelta(weeks=4) - pd.Timedelta(days=1)

# Your date range for the roster
dates = pd.date_range(start=start_date, end=end_date, freq='D')

# (Optional) keep your shifts list as-is
shifts = ["7am - 3pm", "3pm - 11pm", "11pm - 7am"]
