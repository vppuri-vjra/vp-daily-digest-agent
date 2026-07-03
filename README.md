# VP Daily Digest Agents

Two agents that push the same 5 exec-attention subject themes to different channels
every day, each with a body organized into 4 buckets: **Decisions needed**,
**Deadlines**, **Blockers**, **Required actions**.

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
