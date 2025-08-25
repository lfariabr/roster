import streamlit as st

st.set_page_config(
    page_title="MyRoster",
    layout="centered",
    page_icon="📅",
    initial_sidebar_state="collapsed"
)

from views import rosterView

# st.title("Concierge Tool")
# st.markdown("Use the tool below to update your availability process.")

menu = st.sidebar.radio("📂 Select a screen:", [
    "📅 Roster Availability",
])

# ---- View Routing ----
if menu == "📅 Roster Availability":
    rosterView.display()

# ---- Footer (Optional) ----
st.sidebar.markdown("---")
st.sidebar.caption("luisfaria.dev")