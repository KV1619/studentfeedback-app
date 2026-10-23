import sqlite3
from datetime import datetime, date
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "feedback.db"

QUESTIONS = [
    "The course content supports my learning needs.",
    "Lessons and explanations are clear.",
    "The pace of teaching helps me understand the material.",
    "Learning materials and resources are useful.",
    "The workload is manageable.",
    "Assessments reflect what I have learned.",
    "I receive helpful feedback on my progress.",
    "I can access academic support when I need it.",
    "Overall, I am satisfied with my student learning experience.",
]
SCALE = ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]


def connect_db():
    conn = sqlite3.connect(DB_PATH, timeout=20, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                q1 TEXT NOT NULL, q2 TEXT NOT NULL, q3 TEXT NOT NULL,
                q4 TEXT NOT NULL, q5 TEXT NOT NULL, q6 TEXT NOT NULL,
                q7 TEXT NOT NULL, q8 TEXT NOT NULL, q9 TEXT NOT NULL,
                q10 TEXT NOT NULL DEFAULT '',
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def load_feedback():
    with connect_db() as conn:
        return pd.read_sql_query("SELECT * FROM feedback ORDER BY created_at DESC, id DESC", conn)


def inject_css():
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
      html, body, [class*="css"] { font-family: Inter, sans-serif; }
      .stApp {
        background: radial-gradient(ellipse at 8% 0%, #e8eaff 0, transparent 34rem), #f3f5fb;
        color: #172033;
      }
      .block-container { max-width: 1180px; padding-top: 1.6rem; padding-bottom: 3rem; }
      [data-testid="stHeader"] { background: transparent; }
      .brand-row { display:flex; align-items:center; justify-content:space-between; gap:14px; margin-bottom:1.2rem; }
      .brand-left { display:flex; align-items:center; gap:12px; }
      .brand-mark { display:grid; place-items:center; width:46px; height:46px; border-radius:15px;
        background:linear-gradient(145deg,#f0efff,#e5e4ff); color:#504fd2; font-size:23px; border:1px solid #e1e1ff; }
      .brand-title { font-size:17px; font-weight:800; color:#172033; margin:0; }
      .brand-caption { font-size:12px; color:#778198; margin:2px 0 0; }
      .saved-pill { border:1px solid #e5e8f0; border-radius:999px; background:#ffffffb8; padding:8px 12px; color:#667087; font-size:12px; }
      .hero { padding:30px 34px; margin:0 0 18px; border-radius:22px; color:white;
        background:linear-gradient(115deg,#32348e 0%,#4d4cc2 54%,#6860dc 100%);
        box-shadow:0 14px 32px #4546b82b; }
      .hero-kicker { color:#d0ceff; font-size:11px; font-weight:800; letter-spacing:1.5px; text-transform:uppercase; margin:0 0 10px; }
      .hero h1 { font-size:clamp(27px,4vw,36px); line-height:1.15; margin:0 0 9px; color:white; }
      .hero p { color:#e1e2ff; margin:0; font-size:14px; line-height:1.6; }
      .metric { background:white; border:1px solid #e7eaf1; border-radius:16px; padding:17px 18px;
        min-height:105px; box-shadow:0 7px 22px #202b450b; border-top:3px solid #5b5ce2; }
      .metric-label { color:#778198; font-size:12px; font-weight:600; min-height:30px; }
      .metric-value { color:#202943; font-size:26px; font-weight:800; letter-spacing:-.7px; margin-top:5px; }
      div[data-testid="stForm"] { background:white; border:1px solid #e5e8f0; border-radius:17px; padding:22px; }
      .section-title { color:#172033; font-size:18px; font-weight:800; margin:0 0 4px; }
      .section-caption { color:#778198; font-size:13px; margin:0 0 15px; }
      div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
        border-radius:10px; border:0; background:linear-gradient(100deg,#5b5ce2,#6a63e8); color:white;
        font-weight:700; min-height:42px; }
      div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover { color:white; border:0; background:#4849c7; }
      [data-testid="stDataFrame"] { border:1px solid #e7eaf1; border-radius:12px; overflow:hidden; }
      .footnote { text-align:center; color:#858da1; font-size:12px; margin-top:25px; }
      @media (max-width: 700px) { .hero { padding:24px 21px; } .block-container { padding-left:1rem; padding-right:1rem; } }
    </style>
    """, unsafe_allow_html=True)


def metric_card(label, value, accent="#5b5ce2"):
    st.markdown(
        f"""<div class="metric" style="border-top-color:{accent}">
        <div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>""",
        unsafe_allow_html=True,
    )


def save_submission(values):
    columns = [
        "name", "email", "rating", "q1", "q2", "q3", "q4", "q5",
        "q6", "q7", "q8", "q9", "q10", "message", "created_at"
    ]
    placeholders = ",".join(["?"] * len(columns))
    with connect_db() as conn:
        conn.execute(
            f"INSERT INTO feedback ({','.join(columns)}) VALUES ({placeholders})",
            [values[c] for c in columns],
        )
        conn.commit()


def main():
    st.set_page_config(page_title="Student Feedback System", page_icon="✦", layout="wide")
    inject_css()
    init_db()

    st.markdown("""
    <div class="brand-row">
      <div class="brand-left">
        <div class="brand-mark">✦</div>
        <div><p class="brand-title">Student Feedback System</p>
        <p class="brand-caption">Student feedback management</p></div>
      </div>
      <div class="saved-pill">● SQLite database</div>
    </div>
    <div class="hero">
      <p class="hero-kicker">Your voice matters</p>
      <h1>Student feedback dashboard</h1>
      <p>Collect student feedback, track ratings, and keep every response in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_feedback()
    today = date.today()
    if not df.empty:
        dates = pd.to_datetime(df["created_at"], errors="coerce")
        month_mask = (dates.dt.year == today.year) & (dates.dt.month == today.month)
        month_df = df.loc[month_mask]
        avg = f'{df["rating"].mean():.1f} / 5'
        month_avg = f'{month_df["rating"].mean():.1f} / 5' if not month_df.empty else "—"
        five_star = int((df["rating"] == 5).sum())
        month_count = len(month_df)
    else:
        avg, month_avg, five_star, month_count = "—", "—", 0, 0

    metrics = st.columns(5)
    metric_values = [
        ("Total responses", len(df), "#5b5ce2"),
        ("Average rating", avg, "#e2a23b"),
        ("5-star responses", five_star, "#38a885"),
        ("Responses this month", month_count, "#e17b69"),
        ("Monthly average", month_avg, "#7c68d8"),
    ]
    for col, (label, value, color) in zip(metrics, metric_values):
        with col:
            metric_card(label, value, color)

    st.write("")
    form_col, response_col = st.columns([0.82, 1.6], gap="large")

    with form_col:
        st.markdown('<p class="section-title">Leave feedback</p><p class="section-caption">Share your experience. All fields except Question 10 are required.</p>', unsafe_allow_html=True)
        with st.form("feedback_form", clear_on_submit=True):
            name = st.text_input("Name", max_chars=80, placeholder="Your name")
            email = st.text_input("Email", max_chars=254, placeholder="you@example.com")
            rating = st.selectbox("Overall rating", options=[5, 4, 3, 2, 1],
                                  format_func=lambda x: {5:"5 — Excellent",4:"4 — Good",3:"3 — Average",2:"2 — Poor",1:"1 — Very poor"}[x])
            st.markdown("**Feedback questions**")
            answers = []
            for i, question in enumerate(QUESTIONS, start=1):
                answers.append(st.radio(f"{i}. {question}", SCALE, key=f"q{i}", horizontal=False))
            other = st.text_area("10. Other suggestions (optional)", placeholder="Share any other comments or suggestions…", max_chars=1000, height=85)
            message = st.text_area("Your feedback *", placeholder="Tell us what you think…", max_chars=2000, height=110)
            submitted = st.form_submit_button("Submit feedback", use_container_width=True)

        if submitted:
            clean_name, clean_email, clean_message = name.strip(), email.strip(), message.strip()
            if not clean_name or not clean_email or not clean_message:
                st.error("Please complete your name, email, and written feedback.")
            elif "@" not in clean_email or "." not in clean_email.rsplit("@", 1)[-1]:
                st.error("Please enter a valid email address.")
            else:
                values = {
                    "name": clean_name, "email": clean_email, "rating": int(rating),
                    **{f"q{i}": answers[i-1] for i in range(1, 10)},
                    "q10": other.strip(), "message": clean_message,
                    "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                }
                try:
                    save_submission(values)
                    st.success("Thank you — your feedback has been saved.")
                    st.rerun()
                except sqlite3.Error:
                    st.error("Could not save the feedback to the database. Please try again.")

    with response_col:
        header_col, clear_col = st.columns([3, 1])
        with header_col:
            st.markdown('<p class="section-title">Recent responses</p><p class="section-caption">Search, filter, and manage submitted feedback.</p>', unsafe_allow_html=True)
        with clear_col:
            if not df.empty:
                with st.popover("Admin tools"):
                    st.warning("Deleting records cannot be undone.")
                    confirm_clear = st.checkbox("I understand; delete all responses", key="confirm_clear")
                    if st.button("Clear all feedback", disabled=not confirm_clear, type="primary"):
                        with connect_db() as conn:
                            conn.execute("DELETE FROM feedback")
                            conn.commit()
                        st.success("All responses deleted.")
                        st.rerun()

        search = st.text_input("Search responses", placeholder="Search name, email, or feedback…")
        filter_col, sort_col = st.columns(2)
        with filter_col:
            selected_rating = st.selectbox("Filter by rating", ["All ratings", "5 stars", "4 stars", "3 stars", "2 stars", "1 star"])
        with sort_col:
            order = st.selectbox("Sort", ["Newest first", "Oldest first", "Highest rating", "Lowest rating"])

        shown = df.copy()
        if not shown.empty:
            if selected_rating != "All ratings":
                target = int(selected_rating[0])
                shown = shown[shown["rating"] == target]
            if search.strip():
                term = search.strip().casefold()
                search_cols = ["name", "email", "message", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]
                mask = shown[search_cols].fillna("").astype(str).apply(
                    lambda col: col.str.casefold().str.contains(term, regex=False)
                ).any(axis=1)
                shown = shown[mask]
            if order == "Oldest first":
                shown = shown.sort_values(["created_at", "id"], ascending=True)
            elif order == "Highest rating":
                shown = shown.sort_values(["rating", "created_at"], ascending=[False, False])
            elif order == "Lowest rating":
                shown = shown.sort_values(["rating", "created_at"], ascending=[True, False])

        st.caption(f"{len(shown)} response(s) shown")
        if shown.empty:
            st.info("No matching feedback yet. Submitted responses will appear here.")
        else:
            for _, row in shown.iterrows():
                created = pd.to_datetime(row["created_at"], errors="coerce")
                date_label = created.strftime("%d %b %Y, %I:%M %p") if not pd.isna(created) else str(row["created_at"])
                with st.container(border=True):
                    title_col, rating_col = st.columns([3, 1])
                    with title_col:
                        st.markdown(f"**{row['name']}**")
                        st.caption(f"{row['email']} · {date_label}")
                    with rating_col:
                        st.markdown(f"**{'★' * int(row['rating'])}{'☆' * (5-int(row['rating']))}**")
                    st.write(str(row["message"]))
                    with st.expander("View question answers"):
                        for i, question in enumerate(QUESTIONS, start=1):
                            st.markdown(f"**Q{i}. {question}**  \n{row[f'q{i}']}")
                        if str(row["q10"]).strip():
                            st.markdown(f"**Q10. Other suggestions**  \n{row['q10']}")
                    with st.popover("Delete response"):
                        st.warning("This permanently deletes this response.")
                        confirm = st.checkbox("Confirm deletion", key=f"confirm_delete_{int(row['id'])}")
                        if st.button("Delete this response", key=f"delete_{int(row['id'])}", disabled=not confirm):
                            with connect_db() as conn:
                                conn.execute("DELETE FROM feedback WHERE id = ?", (int(row["id"]),))
                                conn.commit()
                            st.rerun()

    st.markdown('<p class="footnote">Student Feedback Management System · Built with Streamlit and SQLite</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
