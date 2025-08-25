import streamlit as st
import pandas as pd
from datetime import timedelta

# ---- ROSTER PERIOD ----
start_date = pd.to_datetime("2025-07-14")
end_date = pd.to_datetime("2025-08-10")

dates = pd.date_range(start=start_date, end=end_date, freq='D')

shifts = ["7am - 3pm", "3pm - 11pm", "11pm - 7am"]