# DigiHaz EWS Workshop — Jupyter Notebooks

**Module 5: Early Warning System Design**

Three interactive notebooks. Open directly in **Google Colab** — no installation, no account needed beyond a Google login.

---

## Open in Google Colab (click to launch)

| # | Notebook | Topic | Time | Link |
|---|----------|-------|------|------|
| 1 | EWS System Architecture Demo | Pipeline, sensor networks, magnitude estimation, warning times | 30 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digihaz/early-warning-system-workshop/blob/main/notebooks/01_ews_system_architecture_demo.ipynb) |
| 2 | Alert Threshold Optimisation ⭐ | ROC curves, cost-benefit analysis, seasonal thresholds | 45 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digihaz/early-warning-system-workshop/blob/main/notebooks/02_alert_threshold_optimisation.ipynb) |
| 3 | Case Study Analysis (Live Data) | USGS earthquake data, ShakeAlert/JMA/SASMEX comparison | 30 min | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digihaz/early-warning-system-workshop/blob/main/notebooks/03_case_study_analysis.ipynb) |

⭐ = assessed assignment (submit to Moodle)

---

## How to Use in Colab

1. Click a badge above → notebook opens in your browser
2. Click **"Copy to Drive"** (top left) to save your own copy
3. Run cells one by one with **Shift+Enter** — or click **Runtime → Run all**
4. Read the explanations between code cells
5. Answer the reflection questions at the end

**That's it — no installation, no terminal, no environment.**

---

## What Each Notebook Does

### Notebook 1 — EWS System Architecture Demo
Visualises the complete EWS data pipeline. Simulates a seismic sensor network
detecting P-waves. Shows how magnitude estimation improves in real-time. Calculates
exactly how many seconds of warning each location receives based on distance.
**Interactive:** change the earthquake magnitude and re-run.

### Notebook 2 — Alert Threshold Optimisation ⭐
The main workshop exercise. Works with 5 years of synthetic river discharge data.
Tests the threshold dilemma (too sensitive / optimal / too conservative).
Builds a full ROC curve, finds the cost-optimal threshold, compares wet vs. dry seasons.
**Assessed:** written reflection submitted to Moodle Module 5 assignment.

### Notebook 3 — Case Study Analysis
Downloads **real earthquake data** from the USGS API (free, no key needed).
Compares seismicity across all three case study regions (USA / Japan / Mexico).
Computes warning times to Los Angeles. Classifies tsunamigenic earthquakes
for the SASMEX region. Falls back to synthetic data automatically if offline.

---

## Libraries Used

All pre-installed on Google Colab — nothing to install:

| Library | Used for |
|---------|----------|
| `numpy` | Numerical computation |
| `pandas` | Data tables and time series |
| `matplotlib` | All plots and maps |
| `scikit-learn` | ROC curve calculation (Notebook 2) |
| `requests` | USGS API calls (Notebook 3) |
| `folium` | Interactive maps (Notebook 3, auto-installed) |

---

*DigiHaz Doctoral Training Programme | University of West Attica | github.com/Digihaz*
