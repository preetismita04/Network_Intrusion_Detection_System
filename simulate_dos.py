# simulate_dos.py — safe, local-only DoS-like data generator
import sqlite3
import random
from datetime import datetime

DB = "alerts.db"

def create_table_if_missing():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS alerts
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time TEXT,
                    proto INTEGER,
                    src_port INTEGER,
                    dst_port INTEGER,
                    length INTEGER,
                    status TEXT)''')
    conn.commit()
    conn.close()

def insert_alert(proto, src_port, dst_port, length, status):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT INTO alerts (time, proto, src_port, dst_port, length, status) VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.now().isoformat(), proto, src_port, dst_port, length, status))
    conn.commit()
    conn.close()

def simulate_dos_burst(burst_size=1000, victim_port=80):
    """Insert many DoS-like rows quickly to simulate a burst on your dashboard."""
    for i in range(burst_size):
        proto = 6  # TCP-like
        src_port = random.randint(1024, 65535)
        dst_port = victim_port
        # DoS packets may be small or oddly large depending on attack type; mix values
        length = random.choice([40, 60, 64, 128, 512, 1500])
        status = "🚨 Simulated DoS"
        insert_alert(proto, src_port, dst_port, length, status)

if __name__ == "__main__":
    create_table_if_missing()
    print("Inserting simulated DoS burst into alerts.db (local only)...")
    simulate_dos_burst(burst_size=500, victim_port=80)
    print("Done — open your Flask dashboard to view the alerts.")
