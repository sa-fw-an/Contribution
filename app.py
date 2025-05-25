import os
import subprocess
import random
from datetime import datetime, timedelta, date

import streamlit as st
def generate_fake_contributions(start_date: date, end_date: date, min_contrib: int, max_contrib: int):
    """
    Create fake GitHub contributions by making commits on a dummy file between start_date and end_date.
    If min_contrib == 0, some days will have zero commits.
    If min_contrib >= 1, each day will have between min_contrib and max_contrib commits.
    """
    if max_contrib < min_contrib:
        raise ValueError("max_contrib must be >= min_contrib")

    repo_path = "."
    os.chdir(repo_path)

    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.min.time())

    all_days = (end_dt - start_dt).days + 1
    dates = [start_dt + timedelta(days=i) for i in range(all_days)]

    for single_day in dates:
        if min_contrib == 0:
            count = random.randint(0, max_contrib)
        else:
            count = random.randint(min_contrib, max_contrib)
        if count == 0:
            continue

        commit_times = []
        for _ in range(count):
            rand_time = single_day + timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59),
            )
            commit_times.append(rand_time)
        commit_times.sort()

        for rand_time in commit_times:
            iso_ts = rand_time.strftime("%Y-%m-%dT%H:%M:%S")
            with open("contribution.txt", "a") as f:
                f.write(f"Contribution at {iso_ts}\n")
            subprocess.run(["git", "add", "contribution.txt"], check=True)
            subprocess.run(
                ["git", "commit", "-m", f"Contribution for {iso_ts}", "--date", iso_ts],
                check=True,
            )
    subprocess.run(["git", "push", "origin", "main"], check=True)
    with open("contribution.txt", "w") as f:
        f.write("")
    subprocess.run(["git", "add", "contribution.txt"], check=True)
    subprocess.run(["git", "commit", "-m", "Reset contribution file"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

def local_css():
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(135deg, #2a4365 0%, #1a365d 100%);
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
        }
        .main-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .main-header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        .generate-btn > button {
            background-color: #4CAF50;
            color: white;
        }
        .generate-btn > button:hover {
            background-color: #3e8e41;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .clear-btn > button {
            background-color: #f6f6f6;
            color: #444;
        }
        .clear-btn > button:hover {
            background-color: #e6e6e6;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .input-section {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #e9ecef;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .date-info {
            padding: 0.75rem;
            background-color: #e8f4f8;
            border-radius: 8px;
            margin-top: 1rem;
            text-align: center;
            border-left: 4px solid #0288d1;
        }
        .stNumberInput {
            margin-top: 0.5rem;
        }
        .footer {
            text-align: center;
            padding-top: 2rem;
            opacity: 0.7;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="GitHub Contribution Generator", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

local_css()

st.markdown("""
<div class="main-header">
    <h1>📈 GitHub Contribution Generator</h1>
    <p>Make your GitHub profile look more active with synthetic contributions</p>
</div>
""", unsafe_allow_html=True)

if "start_date" not in st.session_state:
    st.session_state.start_date = date.today() - timedelta(days=7)
if "end_date" not in st.session_state:
    st.session_state.end_date = date.today()
if "min_contrib" not in st.session_state:
    st.session_state.min_contrib = 1
if "max_contrib" not in st.session_state:
    st.session_state.max_contrib = 5

with st.container():
    st.subheader("⚙️ Configure Contribution Settings")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Date Range**")
        st.session_state.start_date = st.date_input(
            "Start Date", value=st.session_state.start_date
        )
        st.session_state.end_date = st.date_input(
            "End Date", value=st.session_state.end_date
        )
    with col2:
        st.markdown("**Contribution Count**")
        st.session_state.min_contrib = st.number_input(
            "Min Contributions/Day",
            min_value=0,
            max_value=100,
            value=st.session_state.min_contrib,
            step=1,
            help="Minimum number of commits per day"
        )
        st.session_state.max_contrib = st.number_input(
            "Max Contributions/Day",
            min_value=0,
            max_value=100,
            value=st.session_state.max_contrib,
            step=1,
            help="Maximum number of commits per day"
        )

gen_btn, _, clr_btn = st.columns([1, 0.1, 1])
with gen_btn:
    st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
    generate_clicked = st.button("🚀 Generate Contributions")
    st.markdown('</div>', unsafe_allow_html=True)
with clr_btn:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    clear_clicked = st.button("🗑️ Reset Defaults")
    st.markdown('</div>', unsafe_allow_html=True)

if generate_clicked:
    if st.session_state.end_date < st.session_state.start_date:
        st.error("⚠️ End Date must be on or after Start Date.")
    elif st.session_state.max_contrib < st.session_state.min_contrib:
        st.error("⚠️ Max Contributions must be ≥ Min Contributions.")
    else:
        with st.spinner("Generating commits... this may take a while"):
            try:
                generate_fake_contributions(
                    st.session_state.start_date,
                    st.session_state.end_date,
                    st.session_state.min_contrib,
                    st.session_state.max_contrib,
                )
                st.success("🎉 Contributions successfully generated and pushed to GitHub!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error occurred: {e}")

if clear_clicked:
    st.session_state.start_date = date.today() - timedelta(days=7)
    st.session_state.end_date = date.today()
    st.session_state.min_contrib = 1
    st.session_state.max_contrib = 5
    st.experimental_rerun()

st.markdown("""
<div class="footer">
    GitHub Contribution Generator by Safwan Sayeed • Use responsibly
</div>
""", unsafe_allow_html=True)