# AI-Assisted IoT Development 

**Module 7 of the DigiHaz Doctoral Training Programme**

A workshop on building IoT sensor networks for natural hazard monitoring using AI-assisted programming (LLMs such as Claude, ChatGPT, Copilot — workshop is vendor-neutral).

---

Overview

| | |
|---|---|
| **Audience** | PhD students with some Python background, no hardware experience required |
| **Hardware** | ESP32, Raspberry Pi, or Wokwi browser simulator (no physical hardware needed) |
| **Sensors** | MPU6050 (tilt) · BMP280 (pressure) · Capacitive soil moisture |
| **Connects to** | Module 5 — Early Warning System Design |

---

## Structure

| Part | Topic | Time |
|------|-------|------|
| **1** | Foundations of IoT for Hazard Monitoring | 1 hr |
| **2** | The AI-Assisted Coding Workflow + Prompt Engineering | 1.5 hr |
| **3** | Hands-on Build (3 parallel tracks) | 2.5 hr |
| **4** | Integration with Module 5 EWS + Reflection | 1 hr |

---

## Three Parallel Tracks

| Track | Setup | Best For |
|-------|-------|----------|
| **A — ESP32 + MicroPython** | Real hardware kit | Field deployment, battery-powered nodes |
| **B — Raspberry Pi + Python** | Real hardware kit | Edge ML, camera integration, easier debugging |
| **C — Wokwi simulation** | Browser only, no hardware | When hardware unavailable, mobile-friendly |

All three tracks converge on the same MQTT message format so all students see each other's data on a shared dashboard.

---

## Jupyter Notebooks (Run in Google Colab)

| # | Notebook | Description | Time |
|---|----------|-------------|------|
| 1 | Sensor Data Simulation & MQTT Basics | Simulate all three sensors in Python, publish to MQTT | 30 min |
| 2 | **The Vibe Coding Lab** ⭐ | Critique 4 LLM-generated solutions, write your own prompt | 45 min |
| 3 | Cloud Dashboard & EWS Integration | Subscribe to live data, apply thresholds, connect to Module 5 | 30 min |

⭐ = assessed assignment (submit to Moodle)

All notebooks are Colab-ready — click the badge inside the notebook to launch.

---

## Repository Structure

```
topic_04/
├── README.md                                    ← this file
├── SETUP.md                                     ← optional hardware setup guide
│
├── slides/
│   └── IoT_Workshop_DigiHaz.pptx                ← 22-slide deck
│
├── lecture-notes/
│   └── IoT_Lecture_Notes_Module7.docx           ← full lecture notes
│
└── notebooks/
    ├── README.md                                ← Colab links table
    ├── 01_sensor_simulation_mqtt.ipynb
    ├── 02_vibe_coding_lab.ipynb                 ← assessed
    └── 03_dashboard_ews_integration.ipynb
```

---

## Key Concepts

### The 5-Step AI-Assisted Coding Loop
1. **PROMPT** — Describe in plain English what you want
2. **GENERATE** — The LLM writes code for your board
3. **TEST** — Run on hardware or in simulator
4. **DEBUG** — Read error, feed back to AI
5. **ITERATE** — Refine the prompt until working

### Six Ingredients of a Strong Prompt
1. The **board** (ESP32 / Pi / Pico)
2. The **sensor model** (MPU6050, not just "IMU")
3. The **interface and pin** (I²C address, GPIO number)
4. The **timing** (every X seconds)
5. **Calibration or units**
6. The **output destination** (MQTT topic, file, screen)

### Five Common LLM Failure Modes
- **Hallucinated pins** — invented pin numbers
- **Wrong library** — outdated or fake imports
- **Off-by-one bugs** — loop count errors
- **Plausible nonsense** — runs but output is physically impossible
- **Security gaps** — hard-coded passwords, no TLS

### The Trust-or-Verify Boundary
| ✅ Vibe code freely | ⚠ Always verify |
|---|---|
| Data parsing & formatting | Alert threshold logic |
| Plotting & visualisation | Pin assignments & wiring |
| MQTT boilerplate | Sensor calibration formulas |
| JSON/CSV I/O | Power management |
| Dashboard layouts | Network security |
| Documentation | Anything triggering a real alarm |

---

## Connection to Module 5 (EWS)

This module fills the **SENSORS layer** of the EWS pipeline you built in Module 5:

```
SENSORS → Processing → Decision → Dissemination → Response
   ↑
   Your IoT node lives here
```

Module 7 IoT nodes publish to MQTT; the Module 5 EWS processor subscribes, applies threshold optimisation (from Module 5 Notebook 2), and triggers alerts.

---

## License

MIT — see LICENSE file.

---

*DigiHaz Doctoral Training Programme | University of West Attica | github.com/Digihaz*
*Funded by the Global Gateway initiative and the European Union*
