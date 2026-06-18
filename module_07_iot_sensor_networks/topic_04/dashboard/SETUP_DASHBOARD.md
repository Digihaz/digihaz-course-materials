# Grafana Cloud + InfluxDB Dashboard — Setup Guide

**DigiHaz Module 7: AI-Assisted IoT Development**

This guide walks you through setting up the **production-grade dashboard** for your IoT sensor data using Grafana Cloud and InfluxDB Cloud. Both services have generous free tiers that easily accommodate the workshop.

**Time to complete:** ~30 minutes the first time. After that, importing the dashboard takes 2 minutes.

---

## Architecture Overview

```
┌──────────────┐    MQTT    ┌──────────────┐   HTTP    ┌──────────────┐
│  ESP32 / Pi  │──────────▶│   Bridge     │──────────▶│   InfluxDB   │
│   sensors    │            │  (Python)    │            │    Cloud     │
└──────────────┘            └──────────────┘            └──────┬───────┘
                                                                │
                                                                ▼
                                                         ┌──────────────┐
                                                         │   Grafana    │
                                                         │    Cloud     │
                                                         └──────────────┘
                                                                │
                                                                ▼
                                                          shareable URL
                                                          for students
```

**Why two services?** InfluxDB is a time-series database — it stores millions of sensor readings efficiently. Grafana is a visualisation tool — it queries the database and draws the dashboard. They are designed to work together.

**Why the bridge?** Sensors publish to MQTT (lightweight, real-time). InfluxDB receives via HTTP. The bridge is a small Python script that subscribes to MQTT and forwards each message into InfluxDB. We provide it ready-made.

---

## Step 1 — Create an InfluxDB Cloud Account (10 min)

1. Go to **https://cloud2.influxdata.com/signup**
2. Sign up with email (free tier — no credit card required)
3. Choose any provider/region (AWS is fine)
4. Create an organisation: `digihaz` (or your team name)
5. Create a bucket: `digihaz_sensors`
6. **Generate an API token:**
   - Left menu → **API Tokens** → **Generate API Token** → **All Access API Token**
   - Copy the token immediately (you cannot see it again later)
   - Save it as `INFLUX_TOKEN` somewhere safe
7. **Note your connection details:**
   - **URL** — visible at the top of the page (e.g., `https://us-east-1-1.aws.cloud2.influxdata.com`)
   - **Organisation** — the slug you chose
   - **Bucket** — `digihaz_sensors`

You now have a time-series database in the cloud.

---

## Step 2 — Create a Grafana Cloud Account (5 min)

1. Go to **https://grafana.com/auth/sign-up/create-user**
2. Sign up (free tier includes Grafana, no credit card)
3. Create a stack — pick any region close to your students
4. After login, you'll see the Grafana home dashboard

You now have a visualisation server in the cloud.

---

## Step 3 — Connect Grafana to InfluxDB (3 min)

In Grafana:

1. Left menu → **Connections** → **Add new connection**
2. Search for **InfluxDB** → click it → **Add new data source**
3. Fill in:
   - **Name:** `DigiHaz InfluxDB`
   - **Query language:** **Flux**
   - **URL:** your InfluxDB URL from Step 1
   - **Auth:** turn off Basic Auth, turn on **TLS/SSL**
4. Under **InfluxDB Details:**
   - **Organization:** your org slug (e.g., `digihaz`)
   - **Token:** paste the API token from Step 1
   - **Default Bucket:** `digihaz_sensors`
5. Click **Save & test** — you should see "Data source is working"

Grafana can now query your InfluxDB.

---

## Step 4 — Run the MQTT-to-InfluxDB Bridge (5 min)

The bridge subscribes to the workshop MQTT broker and writes incoming messages to InfluxDB. **One person on the team runs it** (often the instructor) — it doesn't matter whose laptop, as long as it stays running.

**Option A — Run locally:**

```bash
pip install paho-mqtt influxdb-client
export INFLUX_URL='https://us-east-1-1.aws.cloud2.influxdata.com'
export INFLUX_TOKEN='your_token_here'
export INFLUX_ORG='digihaz'
export INFLUX_BUCKET='digihaz_sensors'
python mqtt_to_influx_bridge.py
```

You should see:
```
✅ Connected to MQTT broker test.mosquitto.org
📡 Subscribed to digihaz/+/all
✅ Connected to InfluxDB at https://us-east-1-1.aws.cloud2.influxdata.com
[2026-06-14 10:32:01] site_alpha  tilt=2.34°  press=1012.4 hPa  soil=42.1%  → InfluxDB ✓
[2026-06-14 10:32:06] site_beta   tilt=0.85°  press=1008.2 hPa  soil=78.4%  → InfluxDB ✓
...
```

**Option B — Run on a Raspberry Pi (always-on):**

The bridge is small (<100 lines). A Pi Zero W can run it 24/7 for the cost of a USB charger. Same commands as above. We provide a `systemd` unit file in `bridge/` so the bridge auto-starts on boot.

**Option C — Run on a free Oracle Cloud VM:**

If you want zero-maintenance: Oracle Cloud Free Tier gives you 2 always-free Arm VMs. Deploy the bridge there and it runs forever. Setup script in `bridge/oracle_setup.sh`.

---

## Step 5 — Import the Dashboard (2 min)

We provide a pre-built dashboard as a JSON file. To import:

1. In Grafana: left menu → **Dashboards** → **New** → **Import**
2. Click **Upload JSON file** → select `digihaz_dashboard.json` from this repo
3. Choose your `DigiHaz InfluxDB` data source from the dropdown
4. Click **Import**

The dashboard appears with:
- 📊 **4 live sensor panels** (tilt, pressure, soil moisture, alert state) per site
- 🚦 **Alert status indicator** (red/orange/green per site)
- 📅 **24-hour rolling time series** with auto-refresh every 5 seconds
- 🗺️ **Multi-site comparison view**
- 🚨 **Alert rules** that fire when thresholds are crossed

---

## Step 6 — Share with Students (1 min)

Grafana dashboards can be made public with one click:

1. Open your dashboard
2. Top-right → **Share** → **Public dashboard**
3. Toggle **Enable**
4. Copy the public URL

Send the URL to students via Moodle. They can view the dashboard from any browser — **no Grafana account needed on their side.**

**Privacy note:** Public dashboards hide the underlying queries and credentials. Only the panel visualisations are exposed. Anyone with the URL can view but not edit.

---

## Free Tier Limits

| Service | Free tier includes | Workshop usage |
|---------|--------------------|----------------|
| **InfluxDB Cloud** | 30 days data retention, 5 GB writes, 300 MB queries/day | Easily covers a 1-day workshop with 50 students |
| **Grafana Cloud** | 10,000 series, 50 GB logs, 14-day retention | Workshop uses < 1% of this |

If you run the workshop monthly, both stay comfortably within free tiers indefinitely.

---

## Troubleshooting

**Bridge connects but nothing arrives at InfluxDB:**
- Check token has **Write** permission to the bucket
- Check the org name matches exactly (case-sensitive)

**Grafana panels show "No data":**
- Confirm the bucket name in the dashboard variables matches your InfluxDB bucket
- Set the time range to "Last 1 hour" — default of "Last 6 hours" may be empty if you just started

**Students can't see the public dashboard:**
- Check public sharing is enabled in dashboard settings
- The URL must include the random hash; don't truncate it

**No MQTT messages arriving:**
- Confirm students are publishing to `digihaz/{their_name}/all`
- Subscribe with `mosquitto_sub -h test.mosquitto.org -t 'digihaz/#' -v` to verify

---

## Alternative: Use the DigiHaz Shared Dashboard

For the workshop, **the instructor sets up steps 1–5 once**. Students just open the public URL from step 6. They don't need to create any accounts.

This is the recommended approach for the 1-day workshop — keeps friction minimal and lets students focus on building their sensor nodes.

---

*DigiHaz Doctoral Training Programme | University of West Attica*
