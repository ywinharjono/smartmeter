"""
Flask Backend untuk Smart Meter Monitor
Menyediakan API endpoint dan serve dashboard web
"""

from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
from database import (
    init_db, get_latest_reading, get_readings, 
    get_daily_summary, get_alerts
)
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG

app = Flask(__name__)


@app.route('/')
def index():
    """Halaman dashboard utama"""
    return render_template('index.html')


@app.route('/api/current')
def api_current():
    """API: Data real-time terbaru"""
    reading = get_latest_reading()
    if reading:
        return jsonify({
            'success': True,
            'data': reading
        })
    return jsonify({
        'success': False,
        'message': 'No data available'
    }), 404


@app.route('/api/history')
def api_history():
    """API: Data historis"""
    hours = request.args.get('hours', 24, type=int)
    readings = get_readings(hours)
    return jsonify({
        'success': True,
        'count': len(readings),
        'data': readings
    })


@app.route('/api/daily')
def api_daily():
    """API: Ringkasan harian"""
    days = request.args.get('days', 30, type=int)
    summary = get_daily_summary(days)
    return jsonify({
        'success': True,
        'data': summary
    })


@app.route('/api/alerts')
def api_alerts():
    """API: Daftar alert"""
    limit = request.args.get('limit', 50, type=int)
    alerts = get_alerts(limit)
    return jsonify({
        'success': True,
        'data': alerts
    })


@app.route('/api/stats')
def api_stats():
    """API: Statistik ringkas"""
    latest = get_latest_reading()
    daily = get_daily_summary(1)
    
    stats = {
        'current': latest,
        'today_kwh': daily[0]['daily_kwh'] if daily else 0,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'data': stats
    })


def create_app():
    """Factory function untuk Flask app"""
    init_db()
    return app


if __name__ == '__main__':
    init_db()
    print(f"Starting server on http://{FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
