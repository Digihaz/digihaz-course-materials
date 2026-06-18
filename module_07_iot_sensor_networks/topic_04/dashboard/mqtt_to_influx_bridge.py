#!/usr/bin/env python3
"""
DigiHaz MQTT → InfluxDB Bridge
================================

Subscribes to the workshop MQTT broker and forwards all sensor messages
into InfluxDB Cloud, where Grafana can visualise them in real time.

Usage:
    pip install paho-mqtt influxdb-client
    export INFLUX_URL='https://us-east-1-1.aws.cloud2.influxdata.com'
    export INFLUX_TOKEN='your_api_token_here'
    export INFLUX_ORG='digihaz'
    export INFLUX_BUCKET='digihaz_sensors'
    python mqtt_to_influx_bridge.py

The bridge expects MQTT messages on topics matching `digihaz/<site>/all`
with JSON payloads like:

    {
        "ts":         "2026-06-14T10:32:00Z",
        "site":       "site_alpha",
        "tilt_deg":   3.24,
        "press_hpa":  1012.4,
        "soil_pct":   42.1,
        "alert":      "GREEN"
    }

Run it in a terminal that stays open, on a Pi Zero W as a systemd service,
or on a free-tier cloud VM.
"""

import json
import os
import signal
import sys
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# ── CONFIGURATION (override via environment variables) ───────────────────
MQTT_BROKER     = os.getenv('MQTT_BROKER',     'test.mosquitto.org')
MQTT_PORT       = int(os.getenv('MQTT_PORT',   '1883'))
MQTT_TOPIC      = os.getenv('MQTT_TOPIC',      'digihaz/+/all')
MQTT_CLIENT_ID  = os.getenv('MQTT_CLIENT_ID',  f'digihaz-bridge-{int(time.time())}')

INFLUX_URL      = os.getenv('INFLUX_URL')
INFLUX_TOKEN    = os.getenv('INFLUX_TOKEN')
INFLUX_ORG      = os.getenv('INFLUX_ORG',      'digihaz')
INFLUX_BUCKET   = os.getenv('INFLUX_BUCKET',   'digihaz_sensors')

# Fail fast if InfluxDB credentials are missing
if not INFLUX_URL or not INFLUX_TOKEN:
    print('❌ ERROR: Set INFLUX_URL and INFLUX_TOKEN environment variables.')
    print('   See SETUP_DASHBOARD.md for instructions.')
    sys.exit(1)


# ── INFLUXDB CLIENT ───────────────────────────────────────────────────────
print(f'⚙  Connecting to InfluxDB at {INFLUX_URL}...')
influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api     = influx_client.write_api(write_options=SYNCHRONOUS)

try:
    health = influx_client.health()
    if health.status != 'pass':
        print(f'⚠  InfluxDB health check returned: {health.status}')
    else:
        print(f'✅ Connected to InfluxDB ({health.name} v{health.version})')
except Exception as e:
    print(f'❌ Could not reach InfluxDB: {e}')
    sys.exit(1)


# ── STATISTICS ────────────────────────────────────────────────────────────
class Stats:
    def __init__(self):
        self.received = 0
        self.written  = 0
        self.errors   = 0
        self.sites    = set()

    def summary(self):
        return (f'msgs={self.received} written={self.written} '
                f'errors={self.errors} sites={len(self.sites)}')


stats = Stats()


# ── MQTT CALLBACKS ────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'✅ Connected to MQTT broker {MQTT_BROKER}')
        client.subscribe(MQTT_TOPIC)
        print(f'📡 Subscribed to {MQTT_TOPIC}')
    else:
        print(f'❌ MQTT connection failed, code={rc}')


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f'⚠  Unexpected MQTT disconnection (code={rc}); reconnecting...')


def on_message(client, userdata, msg):
    """Parse a JSON message and forward it to InfluxDB as a single Point."""
    stats.received += 1
    try:
        # Parse the JSON payload
        payload = json.loads(msg.payload.decode('utf-8'))
        site = payload.get('site', 'unknown')
        stats.sites.add(site)

        # Use the sensor's own timestamp if available, else now
        ts_str = payload.get('ts')
        try:
            ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00')) if ts_str \
                 else datetime.now(timezone.utc)
        except (ValueError, AttributeError):
            ts = datetime.now(timezone.utc)

        # Build an InfluxDB Point
        # Measurement = "sensors"; tags = site + alert level; fields = numeric values
        point = (
            Point('sensors')
            .tag('site', site)
            .tag('alert', payload.get('alert', 'GREEN'))
            .field('tilt_deg',  float(payload.get('tilt_deg',  0.0)))
            .field('press_hpa', float(payload.get('press_hpa', 0.0)))
            .field('soil_pct',  float(payload.get('soil_pct',  0.0)))
            .time(ts, WritePrecision.S)
        )

        # Optional fields (only present in some payloads)
        if 'temp_c' in payload:
            point = point.field('temp_c', float(payload['temp_c']))
        if 'sim_hour' in payload:
            point = point.field('sim_hour', float(payload['sim_hour']))

        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        stats.written += 1

        # Console feedback
        print(f'[{ts.strftime("%H:%M:%S")}] {site:15} '
              f'tilt={payload.get("tilt_deg",0):5.2f}°  '
              f'press={payload.get("press_hpa",0):7.1f} hPa  '
              f'soil={payload.get("soil_pct",0):5.1f}%  '
              f'alert={payload.get("alert","?"):6}  → InfluxDB ✓')

    except json.JSONDecodeError as e:
        stats.errors += 1
        print(f'⚠  Invalid JSON on {msg.topic}: {e}')
    except Exception as e:
        stats.errors += 1
        print(f'⚠  Failed to write {msg.topic}: {e}')


# ── GRACEFUL SHUTDOWN ────────────────────────────────────────────────────
def handle_shutdown(signum, frame):
    print(f'\n👋 Shutting down. Final stats: {stats.summary()}')
    client.loop_stop()
    client.disconnect()
    influx_client.close()
    sys.exit(0)


signal.signal(signal.SIGINT,  handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)


# ── MAIN LOOP ─────────────────────────────────────────────────────────────
client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True)
client.on_connect    = on_connect
client.on_disconnect = on_disconnect
client.on_message    = on_message

print(f'⚙  Connecting to MQTT broker {MQTT_BROKER}:{MQTT_PORT}...')
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()   # background thread for MQTT

print('🔄 Bridge running. Press Ctrl+C to stop.\n')

# Print stats every 60 seconds while keeping the main thread alive
try:
    while True:
        time.sleep(60)
        print(f'--- 60s stats: {stats.summary()} ---')
except KeyboardInterrupt:
    handle_shutdown(None, None)
