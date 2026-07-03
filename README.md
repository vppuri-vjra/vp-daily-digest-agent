# VP Daily Digest Agents

Three agents:

1. **Email** — 5 exec-attention emails/day, each with a body organized into 4 buckets:
   **Decisions needed**, **Deadlines**, **Blockers**, **Required actions**.
2. **Slack** — the same 5 subject themes, posted daily to a Slack channel.
3. **Calendar** — 1 daily "Digest Consumption" event, a reminder block to actually read #1 and #2.

Subject lines are worded to match this criteria (e.g. for a Gmail filter/label rule):

```
subject:(approval OR decision OR review OR timeline OR deadline OR roadmap OR prioritization)
OR "action required" OR "need your" OR "can you review" OR "please confirm"
```

## The 5 subject themes

| # | Subject theme | Matches |
|---|---|---|
| 1 | Approval needed: Q3 roadmap prioritization | approval, roadmap, prioritization |
| 2 | Decision required: vendor selection timeline | decision, timeline |
| 3 | Can you review the security audit deadline? | review, deadline, "can you review" |
| 4 | Action required — release sign-off blocked | "action required" |
| 5 | Need your input: migration go/no-go — please confirm | "need your", "please confirm" |

Each of the 5 messages/emails has unique bucket content — no repeats across the set.

## Agent 1 — Email (`send_digest_emails.py`)

Sends the 5 messages as HTML emails to `vp.puri@gmail.com` via Gmail SMTP.

```bash
cp .env.example .env   # fill in GMAIL_USER / GMAIL_APP_PASSWORD (Gmail App Password, not your login password)
pip install -r requirements.txt
python3 send_digest_emails.py
```

GitHub Actions: `.github/workflows/daily_digest.yml` — daily at 6:00 AM Pacific (13:00 UTC),
plus `workflow_dispatch`. Requires secrets:

- `GMAIL_USER`
- `GMAIL_APP_PASSWORD`
- `NOTIFY_EMAIL`

## Agent 2 — Slack (`send_slack_digest.py`)

Posts the same 5 subject themes (with Slack-flavored bucket content) as Block Kit
messages to the `#engg-2pm-in` channel via `chat.postMessage`.

```bash
cp .env.example .env   # fill in SLACK_BOT_TOKEN / SLACK_CHANNEL
pip install -r requirements.txt
python3 send_slack_digest.py
```

Requires a Slack bot token with the `chat:write` scope, invited to the target channel.

GitHub Actions: `.github/workflows/daily_slack_digest.yml` — daily at 6:15 AM Pacific (13:15 UTC),
plus `workflow_dispatch`. Requires secrets:

- `SLACK_BOT_TOKEN`
- `SLACK_CHANNEL`

## Agent 3 — Calendar (`create_calendar_event.py`)

Creates exactly 1 event/day, titled **"Digest Consumption"**, at 6:30 AM Pacific for 15
minutes, on the `vp.puri@gmail.com` Google Calendar — a block to actually read the day's
email + Slack digests.

### One-time Google Cloud setup

1. In [Google Cloud Console](https://console.cloud.google.com/), create (or reuse) a project and a **Service Account** (IAM & Admin > Service Accounts).
2. Enable the **Google Calendar API** for that project.
3. Create a JSON key for the service account and download it (Keys > Add Key > JSON).
4. In [Google Calendar](https://calendar.google.com) as `vp.puri@gmail.com`: Settings > find your calendar under "Settings for my calendars" > **Share with specific people** > add the service account's email (looks like `xxx@xxx.iam.gserviceaccount.com`) with permission **"Make changes to events"**.
5. Set `GOOGLE_SERVICE_ACCOUNT_JSON` to the *raw JSON content* of the downloaded key (not a file path) and `CALENDAR_ID` to `vp.puri@gmail.com`.

```bash
cp .env.example .env   # fill in GOOGLE_SERVICE_ACCOUNT_JSON / CALENDAR_ID
pip install -r requirements.txt
python3 create_calendar_event.py
```

GitHub Actions: `.github/workflows/daily_calendar_event.yml` — daily at 5:45 AM Pacific (12:45 UTC,
ahead of the 6:30 AM event time), plus `workflow_dispatch`. Requires secrets:

- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `CALENDAR_ID`
