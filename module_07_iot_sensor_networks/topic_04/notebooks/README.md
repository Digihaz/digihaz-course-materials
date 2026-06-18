# DigiHaz IoT Workshop — Jupyter Notebooks

**Module 7: AI-Assisted IoT Development**

Four interactive notebooks. Open directly in **Google Colab** — no installation, no terminal, no environment setup.

---

## Open in Google Colab (click to launch)

| # | Notebook | Topic | Time | Link |
|---|----------|-------|------|------|
| 1 | Sensor Simulation & MQTT Basics | Simulate MPU6050/BMP280/soil moisture, publish to MQTT | 30 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digihaz/digihaz-course-materials/blob/dev/module_07_iot_sensor_networks/topic_04/notebooks/01_sensor_simulation_mqtt.ipynb) |
| 2 | The Vibe Coding Lab ⭐ | Critique 4 LLM solutions, write your own prompt | 45 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digihaz/digihaz-course-materials/blob/dev/module_07_iot_sensor_networks/topic_04/notebooks/02_vibe_coding_lab.ipynb) |
| 3 | Dashboard & EWS Integration | Query live InfluxDB, build local dashboard, apply thresholds | 30 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digihaz/digihaz-course-materials/blob/dev/module_07_iot_sensor_networks/topic_04/notebooks/03_dashboard_ews_integration.ipynb) |
| 4 | Alert Rules & Dissemination ⭐ | Write alert rules in Python, send real Telegram + browser notifications | 45 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digihaz/digihaz-course-materials/blob/dev/module_07_iot_sensor_networks/topic_04/notebooks/04_alerting_exercise.ipynb) |

⭐ = assessed assignment (submit completed `.ipynb` to Moodle)

---

## How to Use in Colab

1. Click a badge above → notebook opens in your browser
2. Click **"Copy to Drive"** (top-left) to save your own copy
3. Run cells with **Shift+Enter** — or **Runtime → Run all**
4. Read the explanations between code cells
5. Answer the reflection questions / complete the assignments

**No installation. No terminal. Works on phone, tablet, Chromebook.**

---

## What Each Notebook Does

### Notebook 1 — Sensor Simulation & MQTT Basics
Simulates realistic readings from all three workshop sensors entirely in Python. Builds JSON messages, publishes to a public MQTT broker, implements local threshold logic. **No hardware required.**

### Notebook 2 — The Vibe Coding Lab ⭐
The first assessed exercise. Four AI-generated solutions are presented; you find the bugs, classify them by failure mode, then write your own prompt for a new task. **Submit to Moodle.**

### Notebook 3 — Dashboard & EWS Integration
Queries the workshop InfluxDB to fetch live sensor data, builds a local matplotlib mirror of the Grafana dashboard, applies cost-optimised thresholds from Module 5. **Connects Module 7 to Module 5.**

### Notebook 4 — Alert Rules & Dissemination ⭐
The second assessed exercise. Implement a full alert state machine in Python (FIRING / PENDING / RESOLVED), send **real Telegram messages** and **browser push notifications** via ntfy.sh. Compare your Python implementation with the production Grafana setup. Choose one of three extension assignments and submit.

---

## Setup for Notebook 4

Notebook 4 requires two free, one-time setups:

**Telegram bot (5 min):**
- Message @BotFather in Telegram → /newbot → get API token
- Message @userinfobot → get your chat ID

**Browser push via ntfy.sh (1 min):**
- Open `https://ntfy.sh/your-unique-topic-name` in a browser tab
- Optional: install ntfy app on phone, subscribe to same topic

Full instructions are in the notebook itself.

---

## Libraries Used

| Library | Purpose | Pre-installed on Colab? |
|---------|---------|--------------------------|
| `numpy` | Numerical computation | ✅ Yes |
| `pandas` | Time-series data | ✅ Yes |
| `matplotlib` | Plots & dashboards | ✅ Yes |
| `paho-mqtt` | MQTT publish/subscribe | ⚙ Installed by first cell |
| `influxdb-client` | InfluxDB queries (Notebook 3) | ⚙ Installed by first cell |
| `requests` | HTTP for Telegram + ntfy.sh (Notebook 4) | ✅ Yes |

---

*DigiHaz Doctoral Training Programme | University of West Attica | github.com/Digihaz*
