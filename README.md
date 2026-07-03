# VP Daily Digest Agent

Sends 5 emails/day to a VP, each with a distinct subject line and a body organized
into 4 buckets: **Decisions needed**, **Deadlines**, **Blockers**, **Required actions**.

Subject lines are worded to match this criteria (e.g. for a Gmail filter/label rule):

```
subject:(approval OR decision OR review OR timeline OR deadline OR roadmap OR prioritization)
OR "action required" OR "need your" OR "can you review" OR "please confirm"
```

## The 5 emails

| # | Subject theme | Matches |
|---|---|---|
| 1 | Approval needed: Q3 roadmap prioritization | approval, roadmap, prioritization |
| 2 | Decision required: vendor selection timeline | decision, timeline |
| 3 | Can you review the security audit deadline? | review, deadline, "can you review" |
| 4 | Action required — release sign-off blocked | "action required" |
| 5 | Need your input: migration go/no-go — please confirm | "need your", "please confirm" |

Each email's bucket content is unique — no two emails repeat the same items.

## Setup

```bash
cp .env.example .env   # fill in GMAIL_USER / GMAIL_APP_PASSWORD (Gmail App Password, not your login password)
pip install -r requirements.txt
python3 send_digest_emails.py
```

## GitHub Actions

`.github/workflows/daily_digest.yml` runs daily at 6:00 AM Pacific (13:00 UTC) and
can also be triggered manually via `workflow_dispatch`. Requires these repo secrets:

- `GMAIL_USER`
- `GMAIL_APP_PASSWORD`
- `NOTIFY_EMAIL`
