import sqlite3
from datetime import datetime

# ✅ CREATE table only once — when module loads
conn = sqlite3.connect('study_tracker.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        date TEXT,
        subject TEXT,
        hours INTEGER
    )
''')
conn.commit()

def log_study(subject, hours):
    # ✅ Make a new connection for each call
    conn = sqlite3.connect('study_tracker.db', check_same_thread=False)
    c = conn.cursor()
    today = datetime.today().strftime('%Y-%m-%d')
    c.execute("INSERT INTO progress (date, subject, hours) VALUES (?, ?, ?)", (today, subject, hours))
    conn.commit()
    conn.close()
