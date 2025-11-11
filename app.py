from flask import Flask, render_template   
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 10")
    alerts = cursor.fetchall()
    conn.close()
    return render_template('index.html', alerts=alerts)

@app.route('/alerts')
def alerts():
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC")
    alerts = cursor.fetchall()
    conn.close()
    return render_template('alerts.html', alerts=alerts)

if __name__ == '__main__':
    app.run(debug=True)
