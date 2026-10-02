"""
Data Collector untuk Smart Meter Tuya
Mengambil data dari API Tuya Cloud dan menyimpan ke database
"""

import time
import hmac
import hashlib
import json
import requests
from datetime import datetime
from config import (
    TUYA_ACCESS_ID, TUYA_ACCESS_SECRET, TUYA_DEVICE_ID,
    TUYA_API_ENDPOINT, COLLECT_INTERVAL_SECONDS, ALERT_WATT_THRESHOLD
)
from database import init_db, insert_reading, insert_alert


def generate_tuya_token():
    """Generate token untuk autentikasi Tuya API"""
    t = str(int(time.time() * 1000))
    str_to_sign = TUYA_ACCESS_ID + t
    sign = hmac.new(
        TUYA_ACCESS_SECRET.encode('utf-8'),
        str_to_sign.encode('utf-8'),
        hashlib.sha256
    ).hexdigest().upper()
    
    url = f"{TUYA_API_ENDPOINT}/v1.0/token?grant_type=1"
    headers = {
        "client_id": TUYA_ACCESS_ID,
        "sign": sign,
        "t": t,
        "sign_method": "HMAC-SHA256"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data.get('success'):
            return data['result']['access_token']
        else:
            print(f"Token error: {data}")
            return None
    except Exception as e:
        print(f"Token request failed: {e}")
        return None


def get_device_status(token):
    """Ambil status device dari Tuya API"""
    url = f"{TUYA_API_ENDPOINT}/v1.0/devices/{TUYA_DEVICE_ID}/status"
    headers = {
        "client_id": TUYA_ACCESS_ID,
        "access_token": token
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if data.get('success'):
            return data['result']
        else:
            print(f"Device status error: {data}")
            return None
    except Exception as e:
        print(f"Device status request failed: {e}")
        return None


def parse_meter_data(status_data):
    """Parse data meter dari response Tuya"""
    # Mapping DPS (Data Point) - sesuaikan dengan device spesifik
    # Common DPS untuk energy meter: 101=power, 102=voltage, 103=current, 104=total_kwh
    dps = {item['code']: item['value'] for item in status_data}
    
    # Default values
    power_watt = 0
    voltage = 0
    current_ampere = 0
    total_kwh = 0
    power_factor = None
    
    # Coba berbagai kode DPS yang umum
    # Power (Watt)
    for key in ['power', 'cur_power', '101']:
        if key in dps:
            val = dps[key]
            # Tuya kadang kirim dalam 0.1W
            power_watt = val / 10 if val > 10000 else val
            break
    
    # Voltage (V)
    for key in ['voltage', 'cur_voltage', '102']:
        if key in dps:
            val = dps[key]
            voltage = val / 10 if val > 1000 else val
            break
    
    # Current (A)
    for key in ['current', 'cur_current', '103']:
        if key in dps:
            val = dps[key]
            current_ampere = val / 1000 if val > 100 else val / 10
            break
    
    # Total kWh
    for key in ['total_kwh', 'kwh', '104', 'elec_total']:
        if key in dps:
            val = dps[key]
            total_kwh = val / 100 if val > 10000 else val / 10 if val > 1000 else val
            break
    
    # Power Factor
    for key in ['power_factor', 'pf']:
        if key in dps:
            power_factor = dps[key]
            break
    
    return {
        'power_watt': power_watt,
        'voltage': voltage,
        'current_ampere': current_ampere,
        'total_kwh': total_kwh,
        'power_factor': power_factor
    }


def collect_once():
    """Collect satu kali data dari device"""
    print(f"[{datetime.now()}] Collecting data...")
    
    token = generate_tuya_token()
    if not token:
        print("Failed to get token")
        return False
    
    status = get_device_status(token)
    if not status:
        print("Failed to get device status")
        return False
    
    meter_data = parse_meter_data(status)
    print(f"Data: {meter_data}")
    
    # Simpan ke database
    insert_reading(
        meter_data['power_watt'],
        meter_data['voltage'],
        meter_data['current_ampere'],
        meter_data['total_kwh'],
        meter_data['power_factor']
    )
    
    # Cek alert
    if meter_data['power_watt'] > ALERT_WATT_THRESHOLD:
        insert_alert(
            'HIGH_POWER',
            f"Power {meter_data['power_watt']:.0f}W exceeds threshold {ALERT_WATT_THRESHOLD:.0f}W",
            meter_data['power_watt'],
            ALERT_WATT_THRESHOLD
        )
        print(f"ALERT: High power detected!")
    
    return True


def run_collector():
    """Loop utama collector"""
    print("Starting Smart Meter Collector...")
    init_db()
    
    while True:
        try:
            collect_once()
        except Exception as e:
            print(f"Collection error: {e}")
        
        time.sleep(COLLECT_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_collector()
