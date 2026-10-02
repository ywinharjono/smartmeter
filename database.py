"""
Database setup dan operasi untuk Smart Meter Monitor
Menggunakan SQLite untuk penyimpanan time-series data
"""

import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH


def init_db():
    """Inisialisasi database dan tabel yang dibutuhkan"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Tabel untuk data meter
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meter_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            power_watt REAL,
            voltage REAL,
            current_ampere REAL,
            total_kwh REAL,
            power_factor REAL
        )
    ''')
    
    # Tabel untuk alert
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            alert_type TEXT,
            message TEXT,
            value REAL,
            threshold REAL
        )
    ''')
    
    # Index untuk query cepat
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp ON meter_readings(timestamp)
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")


def insert_reading(power_watt, voltage, current_ampere, total_kwh, power_factor=None):
    """Insert pembacaan meter baru"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO meter_readings (power_watt, voltage, current_ampere, total_kwh, power_factor)
        VALUES (?, ?, ?, ?, ?)
    ''', (power_watt, voltage, current_ampere, total_kwh, power_factor))
    
    conn.commit()
    conn.close()


def insert_alert(alert_type, message, value, threshold):
    """Insert alert baru"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO alerts (alert_type, message, value, threshold)
        VALUES (?, ?, ?, ?)
    ''', (alert_type, message, value, threshold))
    
    conn.commit()
    conn.close()


def get_latest_reading():
    """Ambil pembacaan terakhir"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM meter_readings ORDER BY timestamp DESC LIMIT 1
    ''')
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'timestamp': row[1],
            'power_watt': row[2],
            'voltage': row[3],
            'current_ampere': row[4],
            'total_kwh': row[5],
            'power_factor': row[6]
        }
    return None


def get_readings(hours=24):
    """Ambil pembacaan dalam jam terakhir"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM meter_readings 
        WHERE timestamp >= datetime('now', '-{} hours')
        ORDER BY timestamp ASC
    '''.format(hours))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{
        'id': row[0],
        'timestamp': row[1],
        'power_watt': row[2],
        'voltage': row[3],
        'current_ampere': row[4],
        'total_kwh': row[5],
        'power_factor': row[6]
    } for row in rows]


def get_daily_summary(days=30):
    """Ambil ringkasan harian"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            date(timestamp) as date,
            MAX(total_kwh) - MIN(total_kwh) as daily_kwh,
            AVG(power_watt) as avg_watt,
            MAX(power_watt) as max_watt
        FROM meter_readings
        WHERE timestamp >= datetime('now', '-{} days')
        GROUP BY date(timestamp)
        ORDER BY date DESC
    '''.format(days))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{
        'date': row[0],
        'daily_kwh': row[1],
        'avg_watt': row[2],
        'max_watt': row[3]
    } for row in rows]


def get_alerts(limit=50):
    """Ambil alert terakhir"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [{
        'id': row[0],
        'timestamp': row[1],
        'alert_type': row[2],
        'message': row[3],
        'value': row[4],
        'threshold': row[5]
    } for row in rows]


if __name__ == "__main__":
    init_db()
