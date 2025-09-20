import streamlit as st

st.set_page_config(
    page_title="MyRoster",
    layout="centered",
    page_icon="📅",
    initial_sidebar_state="collapsed"
)

from views import rosterViewV1, rosterViewV2, rosterViewV3

# st.title("Concierge Tool")
# st.markdown("Use the tool below to update your availability process.")

menu = st.sidebar.radio("📂 Select a screen:", [
    "📅 Roster Availability",
])

# ---- View Routing ----
if menu == "📅 Roster Availability":
    rosterViewV3.display()

# ---- Footer (Optional) ----
st.sidebar.markdown("---")
st.sidebar.caption("luisfaria.dev")