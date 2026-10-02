"""
Konfigurasi Smart Meter Monitor
Isi credential Tuya IoT Platform di sini atau via environment variable
"""

import os

# Tuya IoT Platform Credentials
# Dapatkan dari https://iot.tuya.com/ -> Cloud -> Project -> Devices
TUYA_ACCESS_ID = os.getenv("TUYA_ACCESS_ID", "YOUR_ACCESS_ID")
TUYA_ACCESS_SECRET = os.getenv("TUYA_ACCESS_SECRET", "YOUR_ACCESS_SECRET")
TUYA_DEVICE_ID = os.getenv("TUYA_DEVICE_ID", "YOUR_DEVICE_ID")

# Tuya API Endpoint (sesuaikan region)
# Common: https://openapi.tuyaeu.com (Europe), https://openapi.tuyaus.com (US)
TUYA_API_ENDPOINT = os.getenv("TUYA_API_ENDPOINT", "https://openapi.tuyaeu.com")

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/meter_data.db")

# Collector Settings
COLLECT_INTERVAL_SECONDS = int(os.getenv("COLLECT_INTERVAL_SECONDS", "300"))  # 5 menit

# Flask Server
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# Alert Thresholds
ALERT_WATT_THRESHOLD = float(os.getenv("ALERT_WATT_THRESHOLD", "3500"))  # Watt
