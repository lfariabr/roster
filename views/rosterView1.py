import streamlit as st
import pandas as pd
import re

from helpers.roster import start_date, end_date, shifts, dates  # your logic

def _human_period(a, b):
    return f"{a:%a %d %b} → {b:%a %d %b} ({(b-a).days+1} days)"

def _init_matrix():
    df = pd.DataFrame(False, index=pd.to_datetime(dates), columns=shifts)
    df.index.name = "Date"
    df = df.reset_index()  # bring Date to column 0
    df.insert(1, "Day", pd.to_datetime(df["Date"]).dt.strftime("%a"))  # now Day is column 1
    return df

def _sanitize_filename(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._ -]", "_", name).strip().replace(" ", "_")
    return safe or "availability"

def display():
    st.title("🗓️ My Roster")
    st.caption("Excel Building Management — Availability Submission")
    st.markdown(
        f"**Roster Period:** `{_human_period(start_date, end_date)}`  "
        f"· **Weeks:** {len(pd.period_range(start_date, end_date, freq='W-MON'))}"
    )
    st.divider()

    # --- Identity ---
    col_a, col_b = st.columns([2, 1])
    with col_a:
        name = st.text_input("Your full name", placeholder="e.g., Luis Faria", key="name")
    with col_b:
        st.text_input("Optional email (for your copy)", placeholder="you@company.com", key="email")

    if "matrix" not in st.session_state:
        st.session_state.matrix = _init_matrix()

    # Helper: slice by week starting Monday
    all_days = pd.to_datetime(st.session_state.matrix["Date"])
    week_starts = pd.date_range(start=all_days.min(), end=all_days.max(), freq="W-MON")
    if all_days.min().weekday() == 0 and (len(week_starts) == 0 or week_starts[0] != all_days.min()):
        week_starts = pd.DatetimeIndex([all_days.min()]).append(week_starts)

    # --- Week tabs ---
    tabs = st.tabs([f"Week {i+1} • {ws:%d %b}" for i, ws in enumerate(week_starts)])

    for i, ws in enumerate(week_starts):
        we = ws + pd.Timedelta(days=6)
        # Mask over the canonical matrix in session_state
        mask = (st.session_state.matrix["Date"] >= ws) & (st.session_state.matrix["Date"] <= we)

        with tabs[i]:
            st.markdown("**Shortcuts**  \n*Apply to this week. You can still tweak individual days below.*")

            c1, c2, c3, c4 = st.columns(4)
            # Apply presets directly to session_state.matrix (so it sticks on the same click)
            with c1:
                if st.button("All mornings", key=f"am_{i}"):
                    st.session_state.matrix.loc[mask, shifts[0]] = True
            with c2:
                if len(shifts) >= 2 and st.button("All afternoons", key=f"pm_{i}"):
                    st.session_state.matrix.loc[mask, shifts[1]] = True
            with c3:
                if st.button("All evenings", key=f"ev_{i}") and len(shifts) >= 1:
                    st.session_state.matrix.loc[mask, shifts[-1]] = True
            with c4:
                if st.button("Clear all", key=f"clr_{i}"):
                    st.session_state.matrix.loc[mask, shifts] = False

            # Pull a fresh view AFTER applying any shortcut
            week_df = st.session_state.matrix.loc[mask].reset_index(drop=True)
            week_df = week_df.loc[:, ["Date", "Day", *shifts]]


            editor = st.data_editor(
                week_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD", disabled=True),
                    "Day": st.column_config.TextColumn("Day", disabled=True),
                    **{s: st.column_config.CheckboxColumn(s) for s in shifts},
                },
                key=f"editor_week_{i}",
            )

            # Write editor changes back to the canonical matrix
            st.session_state.matrix.loc[mask, editor.columns] = editor.values

            yes_count = int(editor[shifts].sum().sum())
            st.caption(f"✅ Selected this week: **{yes_count}** shift(s)")

    st.divider()

    matrix = st.session_state.matrix
    disabled = not name or matrix[shifts].sum().sum() == 0
    if disabled and name:
        st.info("Select at least one shift to enable submission.")

    if st.button("✅ Preview & Submit Availability", disabled=disabled, use_container_width=True):
        long = matrix.melt(id_vars=["Date", "Day"], value_vars=shifts, var_name="Shift", value_name="Available")
        long.insert(0, "Name", name)
        long["Available"] = long["Available"].map({True: "YES", False: "NO"})
        long["Date"] = pd.to_datetime(long["Date"]).dt.strftime("%Y-%m-%d")

        st.success("Preview your availability below:")
        st.dataframe(long, use_container_width=True)

        fname = f"{_sanitize_filename(name)}_{start_date:%Y%m%d}_{end_date:%Y%m%d}.csv"
        st.download_button(
            "⬇️ Download CSV",
            data=long.to_csv(index=False).encode("utf-8"),
            file_name=fname,
            mime="text/csv",
            use_container_width=True,
        )

        total_yes = int((long["Available"] == "YES").sum())
        st.code(
            f"""Availability — {name} — {start_date:%d %b} to {end_date:%d %b}

Hi Team,

Please find attached my availability for the cycle ({start_date:%d %b}–{end_date:%d %b}).
Total available shifts selected: {total_yes}.

Kind regards,
{name}""",
            language="text",
        )
