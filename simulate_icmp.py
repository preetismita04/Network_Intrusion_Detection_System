# simulate_icmp.py — safe, local-only ICMP-like data generator
import sqlite3
import random
from datetime import datetime

DB = "alerts.db"

def create_table_if_missing():
    """Uses the same table schema as simulate_dos.py (no schema changes)."""
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
    cur.execute(
        "INSERT INTO alerts (time, proto, src_port, dst_port, length, status) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), proto, src_port, dst_port, length, status),
    )
    conn.commit()
    conn.close()

def random_icmp_type_code():
    """Return a realistic (type, code) pair for ICMP.
    Common examples: Echo Request (8,0), Echo Reply (0,0), Destination Unreachable (3,1..15).
    """
    choice = random.random()
    if choice < 0.5:
        return (8, 0)   # Echo Request (most common in simple ping-like simulations)
    if choice < 0.75:
        return (0, 0)   # Echo Reply
    # Destination Unreachable with random code (network/host/port/protocol etc.)
    return (3, random.randint(0, 15))

def simulate_icmp_burst(burst_size=500, victim_placeholder_port=0):
    """
    Insert many ICMP-like rows quickly to simulate bursts.
    - proto = 1 (ICMP)
    - src_port/dst_port set to 0 (ICMP doesn't use TCP/UDP ports)
    - length: common ICMP payload sizes
    - status contains type/code and a short description
    """
    icmp_lengths = [28, 56, 64, 100, 512]  # typical ICMP packet sizes (header+payload)
    for i in range(burst_size):
        proto = 1
        src_port = 0
        dst_port = victim_placeholder_port  # keep schema stable; often 0
        length = random.choice(icmp_lengths)
        icmp_type, icmp_code = random_icmp_type_code()
        # Small human-readable status so your dashboard can show what's simulated
        if icmp_type == 8:
            desc = "Echo Request"
        elif icmp_type == 0:
            desc = "Echo Reply"
        elif icmp_type == 3:
            desc = "Dest Unreachable"
        else:
            desc = "Other ICMP"
        status = f"🔔 Simulated ICMP type={icmp_type} code={icmp_code} ({desc})"
        insert_alert(proto, src_port, dst_port, length, status)

if __name__ == "__main__":
    create_table_if_missing()
    print("Inserting simulated ICMP burst into alerts.db (local only)...")
    simulate_icmp_burst(burst_size=500)
    print("Done — open your Flask dashboard to view the alerts.")
