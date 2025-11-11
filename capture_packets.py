from scapy.all import sniff
import pandas as pd
import joblib #used to load random forest model
import sqlite3
from datetime import datetime

# Load trained model
model = joblib.load("nids_model.pkl")

# Connect to SQLite DB
conn = sqlite3.connect("alerts.db", check_same_thread=False)   #The parameter check_same_thread=False allows the same database connection to be accessed from multiple threads — which is necessary because Scapy runs packet capture in different threads.
cursor = conn.cursor()  #creates a cursor object to run sqllite databse queries like insert delete create table
cursor.execute('''CREATE TABLE IF NOT EXISTS alerts
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   time TEXT,
                   proto INTEGER,
                   src_port INTEGER,
                   dst_port INTEGER,
                   length INTEGER,
                   status TEXT)''')

def detect_attack(packet):
    try:
        #packet extraction
        proto = packet.proto if hasattr(packet, 'proto') else 0   # so this line checks whethere the the packet has genuine protocol like 6 for tcp 17 for udp and 1 for icmp and if it is found then the then protocol is exported. and the packet is denoted as 0 because it is safe.
        src_port = packet.sport if hasattr(packet, 'sport') else 0
        dst_port = packet.dport if hasattr(packet, 'dport') else 0
        length = len(packet)
        
        df = pd.DataFrame([[proto, src_port, dst_port, length]], columns=["proto", "src_port", "dst_port", "length"])   #this line is where all your extracted packet information gets combined and prepared for the machine learning model to analyze. and we the data is also trained here using these column names previously in the train model py
        pred = model.predict(df)[0]
        status = "Suspicious" if pred != 0 else "Normal"
        print(f"{datetime.now()} | Proto: {proto} | Src: {src_port} | Dst: {dst_port} | {status}")
        
        if status != "Normal":
            cursor.execute("INSERT INTO alerts (time, proto, src_port, dst_port, length, status) VALUES (?, ?, ?, ?, ?, ?)",
                           (datetime.now(), proto, src_port, dst_port, length, status))
            conn.commit()
    except Exception as e:
        pass      #if there are any exception then dont stop the code just skip the the packet and continue running

print("Starting live packet capture...")
sniff(prn=detect_attack, count=50)   #This line uses Scapy’s sniff() function to capture live network packets from your network interface.
