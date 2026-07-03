#!/usr/bin/env python3
"""
VP Daily Slack Digest Agent

Posts 5 messages/day to a Slack channel, each with a different subject line and a
body organized into 4 buckets: Decisions needed, Deadlines, Blockers, Required actions.

Subjects are worded to match this Gmail-search-style filter (same criteria used by
the email digest agent, send_digest_emails.py):
  subject:(approval OR decision OR review OR timeline OR deadline OR roadmap OR prioritization)
  OR "action required" OR "need your" OR "can you review" OR "please confirm"
"""

import os
from datetime import date

import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "#engg-2pm-in")

TODAY = date.today().strftime("%b %d")

# ── 5 messages: subject + 4 content buckets, each distinct ────────────────────
# Same 5 subject themes as send_digest_emails.py; bucket content rewritten
# shorter/punchier for Slack.

MESSAGES = [
    {
        "subject": f"Approval needed: Q3 roadmap prioritization — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "Payments Reconciliation epic — stays in Q3 or slips to Q4?",
                "Observability vendor pick — cost vs. feature parity.",
            ],
            "Deadlines": [
                "Roadmap locked + shared with stakeholders by end of week.",
                "Q3 budget re-forecast due to Finance in 5 business days.",
            ],
            "Blockers": [
                "Zero Trust rollout stuck on Security sign-off.",
                "Platform team headcount req still pending HR approval.",
            ],
            "Required actions": [
                "Approve final Q3 ranking so eng can start sprint planning.",
                "Flag any reprioritization asks before Thursday's freeze.",
            ],
        },
    },
    {
        "subject": f"Decision required: vendor selection timeline — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "SSO vendor for HR portal — two finalists, both spec-compliant.",
                "Auth-service perf fix: hotfix now or next release train?",
            ],
            "Deadlines": [
                "Vendor contract signed by Friday to hold negotiated pricing.",
                "Perf fix needed before the launch window opens in 10 days.",
            ],
            "Blockers": [
                "Legal review of the vendor MSA running behind — no ETA yet.",
                "CI flaky on ~30% of runs, blocking the perf fix.",
            ],
            "Required actions": [
                "Go/no-go on the SSO vendor so procurement can start the clock.",
                "Weigh in: hotfix vs. release-train timing for the perf fix.",
            ],
        },
    },
    {
        "subject": f"Can you review the security audit deadline? — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "External pen-test firm vs. internal security team?",
                "Audit scope — full infra vs. payments path only?",
            ],
            "Deadlines": [
                "Compliance needs the audit report filed by month-end.",
                "DR runbook updates must close out before audit kickoff.",
            ],
            "Blockers": [
                "Internal security team at capacity (unrelated incident).",
                "External auditor access provisioning takes ~3 days.",
            ],
            "Required actions": [
                "Please review and confirm audit scope by tomorrow.",
                "Sign off on the vendor NDA if we go external.",
            ],
        },
    },
    {
        "subject": f"Action required — release sign-off blocked — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "Cut the release with known CI flakiness, or hold?",
                "Who owns rollback comms if the push-notification fix ships?",
            ],
            "Deadlines": [
                "Release window closes EOD — else it slips a full sprint.",
                "iOS push fix needed before App Store submission.",
            ],
            "Blockers": [
                "CI failing ~1 in 3 builds, root cause still unclear.",
                "QA sign-off blocked — test environment down since this morning.",
            ],
            "Required actions": [
                "Give the explicit go/no-go on today's release cut.",
                "Confirm who owns rollback comms if we ship with known risk.",
            ],
        },
    },
    {
        "subject": f"Need your input: migration go/no-go — please confirm — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "Approve or delay the DB migration cutover given model drift.",
                "Does the recommender rollback plan need its own freeze window?",
            ],
            "Deadlines": [
                "Migration cutover is this weekend — last call-off is Thu noon.",
                "Model drift fix plan needed before migration proceeds.",
            ],
            "Blockers": [
                "Data team hasn't confirmed the rollback script vs. new schema.",
                "k8s autoscaling misconfig still open — may hit migration capacity.",
            ],
            "Required actions": [
                "Please confirm go/no-go for the weekend migration by Thu noon.",
                "Assign an owner to validate the rollback script pre-cutover.",
            ],
        },
    },
]


def build_blocks(subject: str, buckets: dict) -> list:
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": subject, "emoji": True}},
        {"type": "divider"},
    ]
    for bucket_name, items in buckets.items():
        bullet_text = "\n".join(f"• {item}" for item in items)
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{bucket_name}*\n{bullet_text}"},
            }
        )
    blocks.append(
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"Generated by VP Daily Slack Digest Agent · {TODAY}"}],
        }
    )
    return blocks


def post_message(subject: str, blocks: list) -> None:
    if not SLACK_BOT_TOKEN:
        print(f"  SLACK_BOT_TOKEN not set — skipping: {subject}")
        return

    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"},
        json={"channel": SLACK_CHANNEL, "text": subject, "blocks": blocks},
        timeout=15,
    )
    data = resp.json()
    if not data.get("ok"):
        print(f"  FAILED: {subject} — {data.get('error')}")
        return
    print(f"  Posted: {subject}")


def main():
    print(f"VP Daily Slack Digest Agent — posting {len(MESSAGES)} messages to {SLACK_CHANNEL} ({TODAY})")
    for message in MESSAGES:
        blocks = build_blocks(message["subject"], message["buckets"])
        post_message(message["subject"], blocks)
    print("Done.")


if __name__ == "__main__":
    main()
