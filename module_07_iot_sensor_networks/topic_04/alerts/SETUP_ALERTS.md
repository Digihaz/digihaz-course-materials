# Grafana Alert Rules & Dissemination — Setup Guide

**DigiHaz Module 7: AI-Assisted IoT Development**

This guide walks you through configuring **Grafana Cloud alert rules** that automatically fire when sensor thresholds are crossed, and **disseminating those alerts** via Telegram and browser push notifications.

This is the production-style equivalent of the hands-on logic students implement in `notebooks/04_alerting_exercise.ipynb`.

**Time to complete:** ~20 minutes the first time.

---

## What You'll Build

```
┌──────────┐  triggers  ┌──────────────┐  forwards   ┌──────────────┐
│ Grafana  │──alert────▶│  Contact     │────────────▶│  Telegram    │
│  rule    │            │   point      │             │  group/chat  │
└──────────┘            └──────────────┘             └──────────────┘
                                │
                                └──────────────────▶ Browser push
                                                     (Grafana app)
```

When a sensor crosses the threshold (e.g., tilt > 10° AND soil > 90%), Grafana fires an alert. The alert is forwarded to **contact points** — your Telegram chat, browser notification, or both.

---

## Prerequisites

- Working Grafana Cloud setup with the InfluxDB datasource (see `SETUP_DASHBOARD.md`)
- The dashboard imported and showing live data
- A **Telegram account** (free, takes 2 minutes if you don't have one)

---

## Step 1 — Create a Telegram Bot (5 min)

1. In Telegram, search for the user **@BotFather** and start a chat
2. Send: `/newbot`
3. Choose a name: `DigiHaz Alerts` (or anything)
4. Choose a username ending in `bot`: `digihaz_workshop_bot` (must be unique)
5. BotFather replies with an **HTTP API token** like `7891234567:AAGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
6. **Save this token** — you'll need it in Grafana

---

## Step 2 — Get Your Chat ID (3 min)

A bot can send messages to a chat only if it knows the chat ID.

### For personal alerts (just you):
1. Search for the user **@userinfobot** in Telegram and start a chat
2. It replies with your numeric ID (e.g., `123456789`)
3. **Save this as `TELEGRAM_CHAT_ID`**

### For group alerts (workshop class):
1. Create a Telegram group named "DigiHaz Workshop Alerts"
2. Add your new bot to the group as a member
3. Send any message to the group (the bot needs at least one message to find the chat)
4. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser
5. Look for `"chat":{"id":-1001234567890,...` — the **negative** number is your group chat ID
6. **Save this as `TELEGRAM_CHAT_ID`**

**Tip:** test by sending a message yourself:
```bash
curl "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Hello+from+DigiHaz"
```
You should see the message appear in Telegram instantly.

---

## Step 3 — Add the Telegram Contact Point in Grafana (3 min)

1. In Grafana, left menu → **Alerting** → **Contact points**
2. Click **Add contact point**
3. Fill in:
   - **Name:** `DigiHaz Telegram`
   - **Integration:** select `Telegram`
   - **Bot API Token:** paste from Step 1
   - **Chat ID:** paste from Step 2
   - **Message:** (use the template below)

**Recommended message template:**

```
🚨 *DigiHaz Sensor Alert*

{{ range .Alerts }}
*Severity:* {{ .Labels.severity }}
*Site:* {{ .Labels.site }}
*Metric:* {{ .Labels.alertname }}
*Value:* {{ .ValueString }}
*Time:* {{ .StartsAt.Format "15:04:05" }}
{{ end }}

[View dashboard]({{ .ExternalURL }})
```

4. Click **Test** → check Telegram → you should see a test message
5. Click **Save contact point**

---

## Step 4 — Add the Browser Push Contact Point (2 min)

Grafana sends browser notifications via the Grafana web app — students just need the dashboard open in a tab.

1. Still in **Alerting → Contact points**, click **Add contact point**
2. Fill in:
   - **Name:** `DigiHaz Browser`
   - **Integration:** select `Webhook` (we'll point it at Grafana's built-in notifier)
   - **URL:** leave default for in-app notifications
   - Actually, for simpler setup, use **Email** if students provide one, OR use a public push service like ntfy.sh:
     - **Integration:** `Webhook`
     - **URL:** `https://ntfy.sh/digihaz-workshop-{your-name}`
     - **HTTP Method:** `POST`
3. Test → open `https://ntfy.sh/digihaz-workshop-{your-name}` in any browser → notifications appear here

**Why ntfy.sh?** It's free, no signup, works on phones (install the app) and browsers (just bookmark the URL). Perfect for workshops.

---

## Step 5 — Create the Alert Rules (5 min)

Two ways to do this:

### Option A — Import the pre-built rules (recommended)
1. In Grafana, **Alerting** → **Alert rules** → top right **More** → **Import rule definition**
2. Upload `grafana_alert_rules.json` from this folder
3. Choose datasource: `DigiHaz InfluxDB`
4. Choose folder: create one called `DigiHaz`
5. Save

### Option B — Create manually
For each of the 3 rules below, click **New alert rule** and configure:

#### Rule 1: 🚨 Landslide RED Alert
- **Name:** `Landslide RED — Sensor Threshold Breach`
- **Query A:** Flux query (see file)
- **Condition:** when `last()` of A is **above** `0` (the query returns 1 if alert condition met)
- **Folder:** DigiHaz
- **Evaluate every:** `1m` **For:** `2m` (must persist 2 min to avoid noise)
- **Labels:** `severity = critical`, `site = {{ $labels.site }}`
- **Annotations:** Summary and description
- **Contact points:** DigiHaz Telegram + DigiHaz Browser

#### Rule 2: ⚠ Landslide YELLOW Alert
Same as Rule 1 but with the YELLOW threshold logic, `severity = warning`

#### Rule 3: 🌀 Storm Approaching
Pressure trend dropping fast — earlier warning

---

## Step 6 — Test the Alerts (2 min)

The fastest way to verify alerts work is to push synthetic data that crosses the thresholds:

```bash
# From any Python environment
python3 -c "
import paho.mqtt.publish as publish
import json
publish.single(
    'digihaz/test_alert/all',
    json.dumps({
        'site': 'test_alert',
        'tilt_deg': 15.0,        # exceeds 10° threshold
        'press_hpa': 1010.0,
        'soil_pct': 95.0,         # exceeds 90% threshold
        'alert': 'RED'
    }),
    hostname='test.mosquitto.org'
)
print('Sent test alert message')
"
```

Within ~2 minutes (the `For:` duration), you should receive:
- 🚨 A message in your Telegram chat/group
- 🔔 A browser notification (if you set up ntfy.sh)

After the test, send a "back to normal" message:
```python
publish.single('digihaz/test_alert/all',
    json.dumps({'site':'test_alert','tilt_deg':0.5,'press_hpa':1013,'soil_pct':40,'alert':'GREEN'}),
    hostname='test.mosquitto.org')
```

Grafana sends a **Resolved** notification after the next evaluation.

---

## Alert Rules Reference

| Rule | Condition | Severity | Channels | Frequency |
|------|-----------|----------|----------|-----------|
| 🚨 Landslide RED | tilt > 10° AND soil > 90% | critical | Telegram + Browser | Every 1 min, requires 2 min sustained |
| ⚠ Landslide YELLOW | tilt > 5° AND soil > 80% | warning | Telegram | Every 1 min, requires 2 min sustained |
| 🌀 Storm Approaching | pressure trend < -2 hPa/hr | warning | Browser | Every 5 min |
| 📡 Sensor Offline | no data for 10 min | info | Browser | Every 5 min |

---

## Free Tier Notes

- **Telegram:** unlimited messages, free forever
- **ntfy.sh:** free, no account, no message limits for normal use
- **Grafana Cloud:** free tier includes 100 alert rules — workshop uses 4

---

## Troubleshooting

**Alert doesn't fire even though threshold is crossed:**
- Check the `For:` duration — alerts must persist this long to fire (default 2 min)
- Check the alert rule state in Alerting → Alert rules — should show `Firing` not `Pending`
- Verify the Flux query returns data: paste it into Explore tab to test

**Telegram message doesn't arrive:**
- Re-test the bot with the curl command from Step 2
- Check bot is **in** the group (must be added as member, not just invited)
- Verify the chat ID is correct, including the leading minus sign for groups

**ntfy.sh notifications don't appear:**
- Open the topic URL in a browser tab and leave it open
- Install the ntfy.sh app on phone, subscribe to the same topic
- Topic names are public — anyone with the name can subscribe and post, so use something obscure

---

## Linking Back to Module 5

These alert rules are the **DISSEMINATION** layer of the EWS pipeline from Module 5:

```
SENSORS → PROCESSING → DECISION → DISSEMINATION → RESPONSE
   ↑          ↑           ↑            ↑              ↑
  IoT      Bridge +    Threshold    Telegram     People
  nodes    InfluxDB    rules        + browser    take action
                       (Grafana)    push
```

In a real EWS, the dissemination channel is whatever reaches the right people fastest — official SMS, cell broadcast, sirens. The workshop uses Telegram + browser push because they're free and instant, but the **architecture is identical** to a production system.

---

*DigiHaz Doctoral Training Programme | University of West Attica*
