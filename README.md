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
minutes, on the calendar owner's Google Calendar — a block to actually read the day's
email + Slack digests.

Auth is OAuth2 (not a service account key) — it authenticates as the calendar owner
directly via a refresh token, so `CALENDAR_ID` is just `primary` and no calendar-sharing
step is needed. (A service-account-key approach was tried first but blocked by this
Google Cloud org's `iam.disableServiceAccountKeyCreation` policy.)

### One-time Google Cloud setup

1. In [Google Cloud Console](https://console.cloud.google.com/), in your project: **APIs & Services > Library**, search for and enable the **Google Calendar API**.
2. **APIs & Services > OAuth consent screen** — configure it (External or Internal, Testing mode is fine) if not already done.
3. **APIs & Services > Credentials > Create Credentials > OAuth client ID** — Application type: **Desktop app**. Note the Client ID and Client Secret.
4. Put `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET` in `.env`.
5. Run `python3 get_refresh_token.py` locally — it opens a browser, you sign in as the calendar owner and grant calendar access, and it prints a refresh token.
6. Put that refresh token in `.env` as `GOOGLE_OAUTH_REFRESH_TOKEN`, and set `CALENDAR_ID=primary`.

```bash
cp .env.example .env   # fill in GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET
pip install -r requirements.txt
python3 get_refresh_token.py     # one-time — prints GOOGLE_OAUTH_REFRESH_TOKEN
python3 create_calendar_event.py
```

GitHub Actions: `.github/workflows/daily_calendar_event.yml` — daily at 5:45 AM Pacific (12:45 UTC,
ahead of the 6:30 AM event time), plus `workflow_dispatch`. Requires secrets:

- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `GOOGLE_OAUTH_REFRESH_TOKEN`
- `CALENDAR_ID` (`primary`)
