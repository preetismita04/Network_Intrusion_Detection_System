# check_icmp.py
import sqlite3

db = "alerts.db"
conn = sqlite3.connect(db)
cur = conn.cursor()

print("\n🔹 Count of alerts per protocol:\n")
for row in cur.execute("SELECT proto, COUNT(*) FROM alerts GROUP BY proto;"):
    print(f"Protocol {row[0]} → {row[1]} rows")

print("\n🔹 Sample ICMP (proto=1) rows:\n")
for row in cur.execute("SELECT id, time, proto, src_port, dst_port, length, status FROM alerts WHERE proto=1 ORDER BY id DESC LIMIT 10;"):
    print(row)

conn.close()
