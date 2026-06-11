# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:45:22 2026

@author: Buhle Skosana
"""
from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---- DATABASE ------#
def init_db():
    conn = sqlite3.connect("alerts.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT,
            description TEXT,
            reporter_name TEXT,
            location TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---- Get Alerts ----#
@app.route("/api/alerts", methods=['GET'])
def get_alerts():
    conn = sqlite3.connect("alerts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    alerts = []
    for row in rows:
        alerts.append({
            "id":          row[0],
            "type":        row[1],  
            "description": row[2],
            "reporter":    row[3],
            "location":    row[4],
            "time":        row[5],
        })
    return jsonify(alerts)

# ---- REPORT ALERT ----#
@app.route("/api/report", methods=['POST'])  
def report_alert():
    data = request.get_json()
    reporter = data.get("reporter", "Anonymous")

    conn = sqlite3.connect("alerts.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alerts (alert_type, description, reporter_name, location)
        VALUES (?, ?, ?, ?)
        """, (
            data["alert_type"],   
            data["description"],
            data["reporter"],
            data["location"],
        ))
    conn.commit()
    conn.close()

    return jsonify({"message": "Alert added successfully"})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5500))
    app.run(host="0.0.0.0", port=port)
            
