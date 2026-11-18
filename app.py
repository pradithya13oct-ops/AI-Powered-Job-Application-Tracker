import streamlit as st
import sqlite3
from datetime import date
import Database as db

# Page Configuration
st.set_page_config(
    page_title="AI Job Application Tracker",
    page_icon="💼",
    layout="wide"
)

# Database Connection
conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

# Create Jobs Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    role TEXT,
    location TEXT,
    job_type TEXT,
    status TEXT,
    applied_date TEXT,
    job_link TEXT,
    notes TEXT
)
""")

conn.commit()

# Application Title
st.title("💼 AI-Powered Job Application Tracker")
st.subheader("Track your job applications smartly with AI 🚀")

st.divider()

# Sidebar
st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Choose an Option",
    [
        "Dashboard",
        "Add Application",
        "View Applications",
        "AI Career Assistant"
    ]
)

# Dashboard
if menu == "Dashboard":

    st.header("📊 Job Application Dashboard")

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status='Applied'"
    )
    applied = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status='Interview'"
    )
    interview = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status='Selected'"
    )
    selected = cursor.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Applications", total)
    col2.metric("Applied", applied)
    col3.metric("Interviews", interview)
    col4.metric("Selected", selected)

# Add Application
elif menu == "Add Application":

    st.header("➕ Add New Job Application")

    with st.form("job_form"):

        company = st.text_input("Company Name")
        role = st.text_input("Job Role")
        location = st.text_input("Location")

        job_type = st.selectbox(
            "Job Type",
            ["Full-Time", "Internship", "Remote", "Hybrid"]
        )

        status = st.selectbox(
            "Application Status",
            ["Applied", "Interview", "Selected", "Rejected", "Pending"]
        )

        applied_date = st.date_input(
            "Applied Date",
            value=date.today()
        )

        job_link = st.text_input("Job URL")
        notes = st.text_area("Additional Notes")

        submit = st.form_submit_button("Save Application")

        if submit:

            if company and role:

                cursor.execute("""
                INSERT INTO jobs
                (company, role, location, job_type,
                status, applied_date, job_link, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    company,
                    role,
                    location,
                    job_type,
                    status,
                    str(applied_date),
                    job_link,
                    notes
                ))

                conn.commit()

                st.success("Job Application Saved Successfully! 🎉")

            else:
                st.error("Please enter Company Name and Job Role.")

# View Applications
elif menu == "View Applications":

    st.header("📋 Your Job Applications")

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    jobs = cursor.fetchall()

    if jobs:

        for job in jobs:

            with st.expander(f"{job[1]} - {job[2]}"):

                st.write("📍 Location:", job[3])
                st.write("💼 Job Type:", job[4])
                st.write("📌 Status:", job[5])
                st.write("📅 Applied Date:", job[6])
                st.write("🔗 Job URL:", job[7])
                st.write("📝 Notes:", job[8])

    else:
        st.info("No job applications found.")

# AI Career Assistant
elif menu == "AI Career Assistant":

    st.header("🤖 AI Career Assistant")

    st.write(
        "Your personal AI assistant for job search and career guidance."
    )

    question = st.text_area(
        "Ask your career-related question"
    )

    if st.button("Get AI Advice"):

        if question:
            st.info(
                "AI integration will be added in the next development stage."
            )
        else:
            st.warning("Please enter your question.")

conn.close()