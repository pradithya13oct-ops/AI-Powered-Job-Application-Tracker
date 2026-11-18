import sqlite3

# Database Connection
def get_connection():
    conn = sqlite3.connect("jobs.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create Database Table
def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            job_type TEXT,
            status TEXT,
            applied_date TEXT,
            job_link TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


# Add Job Application
def add_job(company, role, location, job_type,
            status, applied_date, job_link, notes):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs (
            company, role, location, job_type,
            status, applied_date, job_link, notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        company, role, location, job_type,
        status, applied_date, job_link, notes
    ))

    conn.commit()
    conn.close()


# View All Applications
def get_all_jobs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")

    jobs = cursor.fetchall()

    conn.close()

    return jobs


# Delete Job Application
def delete_job(job_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM jobs WHERE id = ?",
        (job_id,)
    )

    conn.commit()
    conn.close()


# Update Application Status
def update_status(job_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status = ?
        WHERE id = ?
    """, (status, job_id))

    conn.commit()
    conn.close()


# Get Dashboard Statistics
def get_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status = 'Applied'"
    )
    applied = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status = 'Interview'"
    )
    interview = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE status = 'Selected'"
    )
    selected = cursor.fetchone()[0]

    conn.close()

    return total, applied, interview, selected


# Initialize Database
create_table()