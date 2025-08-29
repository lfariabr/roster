import streamlit as st
import pandas as pd
import re

from helpers.roster import start_date, end_date, shifts, dates  # your logic

def _human_period(a, b):
    return f"from: {a:%a %d %b} → to: {b:%a %d %b} ({(b-a).days+1} days)"

def _init_matrix():
    df = pd.DataFrame(False, index=pd.to_datetime(dates), columns=shifts)
    df.index.name = "Date"
    df = df.reset_index()  # bring Date to column 0
    df.insert(1, "Day", pd.to_datetime(df["Date"]).dt.strftime("%a"))  # Day is column 1
    # Harden dtypes
    for s in shifts:
        df[s] = df[s].astype("boolean")  # pandas nullable boolean
    return df

def _sanitize_filename(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._ -]", "_", name).strip().replace(" ", "_")
    return safe or "availability"

def display():
    st.logo("/workspaces/roster/public/excelBM.jpeg", )
    st.title("ExcelBM's Roster")
    # st.caption("Excel Building Management")
    st.caption("🗓️ Your new way to Submit Shift Availability")
    st.markdown(
        f"**Roster Period:** "
    )
    st.markdown(f"`{_human_period(start_date, end_date)}`"
                )
    st.markdown(f"**Weeks:** {len(pd.period_range(start_date, end_date, freq='W-MON'))}"
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

    if name:
        st.success(f"Hello, **{name}**! Your availability matrix is ready below.")

        # Helper: slice by week starting Monday
        all_days = pd.to_datetime(st.session_state.matrix["Date"])
        week_starts = pd.date_range(start=all_days.min(), end=all_days.max(), freq="W-MON")
        if all_days.min().weekday() == 0 and (len(week_starts) == 0 or week_starts[0] != all_days.min()):
            week_starts = pd.DatetimeIndex([all_days.min()]).append(week_starts)
        
        # ---- Global counters / progress (before tabs) ----
        shift_cols = [s for s in shifts if s in st.session_state.matrix.columns]
        total_days = len(st.session_state.matrix)
        total_shifts_selected = int(st.session_state.matrix[shift_cols].sum().sum())
        days_selected = int(st.session_state.matrix[shift_cols].any(axis=1).sum())
        coverage_pct = (days_selected / total_days * 100) if total_days else 0

        st.markdown(f"**Total shifts selected:** {total_shifts_selected}  \n"
                    f"**Days with at least one shift:** {days_selected} / {total_days} ({coverage_pct:.1f}%)")
        st.progress(coverage_pct / 100 if coverage_pct else 0)
        st.caption("💡**Tip**"": Double tap the buttons below to see your progress.")

        # --- Week tabs ---
        tabs = st.tabs([f"**Week {i+1}:** {ws:%d %b}" for i, ws in enumerate(week_starts)])

        # Stage edits per week; don't write back during render
        staged = {}

        for i, ws in enumerate(week_starts):
            we = ws + pd.Timedelta(days=6)
            mask = (st.session_state.matrix["Date"] >= ws) & (st.session_state.matrix["Date"] <= we)

            with tabs[i]:
                c1, c2, c3, c4 = st.columns(4)

                # Apply presets directly to the canonical matrix (single click)
                with c1:
                    if st.button("All mornings 🌅", key=f"am_{i}"):
                        st.session_state.matrix.loc[mask, shifts[0]] = True
                with c2:
                    if len(shifts) >= 2 and st.button("All afternoons ☀️", key=f"pm_{i}"):
                        st.session_state.matrix.loc[mask, shifts[1]] = True
                with c3:
                    if st.button("All evenings 🌙", key=f"ev_{i}") and len(shifts) >= 1:
                        st.session_state.matrix.loc[mask, shifts[-1]] = True
                with c4:
                    if st.button("Clear all ⛔", key=f"clr_{i}"):
                        st.session_state.matrix.loc[mask, shifts] = False

                # Fresh view AFTER shortcuts
                week_df = st.session_state.matrix.loc[mask].reset_index(drop=True)
                week_df = week_df.loc[:, ["Date", "Day", *shifts]]

                # Ensure checkbox columns are clean booleans and NaN-free each run
                for s in shifts:
                    week_df[s] = week_df[s].fillna(False).astype("boolean")

                editor = st.data_editor(
                    week_df,
                    use_container_width=True,
                    hide_index=True,
                    num_rows="fixed",  # prevents row reflow that can steal the first click
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="YYYY-MM-DD", disabled=True),
                        "Day": st.column_config.TextColumn("Day", disabled=True),
                        **{s: st.column_config.CheckboxColumn(s, default=False) for s in shifts},
                    },
                    column_order=["Date", "Day", *shifts],
                    key=f"editor_week_{i}",
                )

                # Defer syncing this week's edits
                staged[i] = editor.copy()

                yes_count = int(editor[shifts].sum().sum())
                st.caption(f"✅ Selected this week: **{yes_count}** shift(s)")

        # ---- One-shot write-back (prevents double-click behavior) ----
        for i, ws in enumerate(week_starts):
            editor = staged.get(i)
            if editor is None:
                continue
            we = ws + pd.Timedelta(days=6)
            mask = (st.session_state.matrix["Date"] >= ws) & (st.session_state.matrix["Date"] <= we)
            shift_cols = [s for s in shifts if s in editor.columns]
            # Commit only shift columns as pure booleans
            st.session_state.matrix.loc[mask, shift_cols] = editor[shift_cols].fillna(False).astype(bool).to_numpy()

        # Keep dtypes stable globally
        for s in shifts:
            st.session_state.matrix[s] = st.session_state.matrix[s].fillna(False).astype(bool)

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
