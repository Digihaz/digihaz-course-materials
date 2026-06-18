# DigiHaz Alert Response Runbook

This runbook describes what to do when each DigiHaz alert fires. Real production EWS deployments require a runbook for every alert — it's the difference between an alert that triggers action and one that just adds to the noise.

---

## 🚨 Landslide RED — Critical Threshold Breach

**What it means:** Tilt has exceeded 10° AND soil moisture has exceeded 90% at the same site for at least 2 minutes. The conditions for landslide initiation are present.

**Immediate actions:**

1. **Verify the alert is real.** Check the dashboard for the affected site:
   - Is the tilt trace climbing steadily, or did it spike then return to normal?
   - Is the soil moisture trace at saturation, or recovering?
   - Is there other corroborating evidence (recent rainfall, neighbouring sites)?
2. **If real:** activate the local emergency response protocol. The decision authority is the local civil protection authority, not the EWS operator.
3. **If sensor malfunction suspected:** silence the alert (Grafana → Alerting → Silences), dispatch a maintenance team to inspect the sensor, and continue monitoring with neighbouring sites.

**Common causes of false RED alerts:**
- Animal or human contact with the tilt sensor pole
- Sensor mounting drift after temperature swings
- Soil moisture sensor probe contacting roots or rocks

**Escalation:** if RED persists > 30 minutes with corroborating evidence, escalate to regional civil protection authority.

---

## ⚠ Landslide YELLOW — Elevated Risk

**What it means:** Tilt > 5° AND soil > 80% sustained 2+ minutes. The site is in an elevated risk state but hasn't crossed the imminent-danger threshold.

**Immediate actions:**

1. Check the dashboard to confirm the alert. Note the trajectory:
   - Is the site approaching RED? (tilt and soil both still climbing)
   - Is it stable at YELLOW? (oscillating but not climbing)
   - Is it recovering? (heading back below threshold)
2. Increase monitoring frequency mentally; check the dashboard every 15 minutes
3. Verify evacuation routes are clear for the area downslope of the site
4. Notify the on-call response team but do not trigger evacuation yet
5. If YELLOW persists > 6 hours or progresses to RED, follow the RED runbook above

**False alarm rate:** Workshop default threshold produces approximately 10–20% false alarms (this is what the ROC curve from Module 5 optimises). Each YELLOW should be treated seriously but not necessarily acted upon at the level of an evacuation.

---

## 🌀 Storm Approaching — Pressure Drop

**What it means:** Atmospheric pressure has dropped more than 2 hPa per hour, sustained for 5+ minutes. A storm system is approaching the area.

**Why it matters:** the storm itself isn't the landslide hazard — but the rainfall that follows usually saturates soil within 6–24 hours. This is your early-warning lead time to prepare for likely YELLOW/RED alerts later.

**Immediate actions:**

1. Check rainfall forecasts for the affected area (link the local meteorological service in the runbook for your region)
2. Confirm the BMP280 is in a sheltered, ventilated location (sudden pressure drops can be caused by HVAC, doors closing, etc.)
3. Pre-position emergency response resources if the rainfall forecast supports it
4. No public alert at this stage — the lead time is too long and uncertainty too high

**False alarm rate:** higher than landslide alerts because atmospheric pressure is noisy. Cross-reference with weather service forecasts before acting.

---

## 📡 Sensor Offline — No Data

**What it means:** No measurements have been received from a site in 10+ minutes.

**Possible causes (most common first):**

1. **WiFi disconnection** — most common. Check the WiFi router and signal strength.
2. **Battery depletion** — check the node's battery; ESP32 nodes on solar should be checked every 2 weeks
3. **Software crash** — try power-cycling the node. If it crashes again immediately, dump the serial log.
4. **MQTT broker issue** — confirm the broker is reachable; check the bridge process is running
5. **InfluxDB ingestion failure** — check `digihaz-bridge.service` logs on the gateway

**Actions:**

1. Open the dashboard panel for the affected site — confirm gap in data
2. Try to ping the node (if it has a known IP) or check its access point's client list
3. If unreachable, dispatch a physical check
4. If you can reach the node remotely, check the MQTT publish logs

**Time to repair:** Workshop SLO is 24h. For a real EWS, target is 4 hours.

---

## Adding New Runbook Entries

When you add a new alert rule, add a corresponding section here. Each runbook entry should answer four questions:

1. **What does this alert mean** (in plain language, what physical condition is happening)?
2. **What should the responder do immediately?**
3. **What are the common false-alarm causes?**
4. **When should it be escalated?**

A useful rule of thumb: if you can't write a runbook entry for an alert, you probably shouldn't be creating that alert. Alerts without runbooks tend to become noise that responders learn to ignore.

---

*DigiHaz Doctoral Training Programme | University of West Attica*
