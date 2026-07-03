#!/usr/bin/env python3
"""
VP Daily Digest Agent

Sends 5 emails/day to a VP, each with a different subject line and a body
organized into 4 buckets: Decisions needed, Deadlines, Blockers, Required actions.

Subjects are deliberately worded to match this Gmail search filter:
  subject:(approval OR decision OR review OR timeline OR deadline OR roadmap OR prioritization)
  OR "action required" OR "need your" OR "can you review" OR "please confirm"
"""

import os
import smtplib
import ssl
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import certifi
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD", "")
NOTIFY_TO = os.environ.get("NOTIFY_EMAIL", "vp.puri@gmail.com")

TODAY = date.today().strftime("%b %d")

# ── 5 emails: subject + 4 content buckets, each distinct ──────────────────────

EMAILS = [
    {
        "subject": f"Approval needed: Q3 roadmap prioritization — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "Confirm whether the Payments Reconciliation epic stays in Q3 scope or slips to Q4.",
                "Pick between two vendor options for the new observability stack (cost vs. feature parity).",
            ],
            "Deadlines": [
                "Roadmap must be locked and circulated to stakeholders by end of week.",
                "Budget re-forecast for Q3 initiatives due to Finance in 5 business days.",
            ],
            "Blockers": [
                "Waiting on Security sign-off before the Zero Trust rollout can be sequenced into the roadmap.",
                "Headcount request for the platform team still pending HR approval.",
            ],
            "Required actions": [
                "Approve final Q3 initiative ranking so engineering can start sprint planning.",
                "Reply with any reprioritization requests before the roadmap freezes Thursday.",
            ],
        },
    },
    {
        "subject": f"Decision required: vendor selection timeline — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "Select the SSO vendor for the HR portal integration — two finalists, both spec-compliant.",
                "Decide whether the auth-service performance fix ships as a hotfix or waits for the next release train.",
            ],
            "Deadlines": [
                "Vendor contract must be signed by next Friday to hold the negotiated pricing.",
                "Auth-service fix needs to land before the marketing launch window opens in 10 days.",
            ],
            "Blockers": [
                "Legal review of the vendor MSA is running behind — no ETA yet from the legal team.",
                "Performance fix is blocked on a flaky CI pipeline that's failing ~30% of runs.",
            ],
            "Required actions": [
                "Give the go/no-go on the SSO vendor so procurement can start the contract clock.",
                "Weigh in on hotfix vs. release-train timing for the auth-service fix.",
            ],
        },
    },
    {
        "subject": f"Can you review the security audit deadline? — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "Decide whether to bring in an external pen-testing firm or run the audit with the internal security team.",
                "Approve scope: full infrastructure audit vs. targeted review of the payments path only.",
            ],
            "Deadlines": [
                "Compliance requires the audit report filed by month-end.",
                "On-call runbook updates for DR scenarios need to close out before the audit kickoff.",
            ],
            "Blockers": [
                "Internal security team is at capacity through next week due to an unrelated incident.",
                "Access provisioning for the external auditor (if chosen) takes ~3 days to complete.",
            ],
            "Required actions": [
                "Please review and confirm the audit scope by tomorrow so we can book resources.",
                "Sign off on the external vendor NDA if we go with a third-party auditor.",
            ],
        },
    },
    {
        "subject": f"Action required — release sign-off blocked — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "Decide whether to cut the release with the known CI flakiness or hold for a fix.",
                "Determine rollback owner for the mobile push notification fix if the release goes out.",
            ],
            "Deadlines": [
                "Release window closes end of day — after that it slips to next sprint's train.",
                "iOS push notification bug needs a fix or a documented workaround before App Store submission.",
            ],
            "Blockers": [
                "CI pipeline flakiness is causing ~1 in 3 builds to fail without a clear root cause yet.",
                "QA sign-off is blocked on a test environment that's been down since this morning.",
            ],
            "Required actions": [
                "Give the explicit go/no-go for today's release cut.",
                "Confirm who owns rollback communication if we ship with known risk.",
            ],
        },
    },
    {
        "subject": f"Need your input: migration go/no-go — please confirm — {TODAY}",
        "buckets": {
            "Decisions needed": [
                "Approve or delay the database migration cutover date given the current ML model drift issue.",
                "Decide if the recommender service rollback plan needs a dedicated freeze window.",
            ],
            "Deadlines": [
                "Migration cutover is scheduled for this weekend — last checkpoint to call it off is Thursday noon.",
                "Model drift investigation needs a resolution plan documented before the migration proceeds.",
            ],
            "Blockers": [
                "Data team hasn't confirmed the rollback script has been tested against the new schema.",
                "k8s node auto-scaling misconfiguration is still unresolved and could affect migration capacity.",
            ],
            "Required actions": [
                "Please confirm go/no-go for the weekend migration by Thursday noon.",
                "Assign an owner to validate the rollback script before cutover.",
            ],
        },
    },
]


def build_html_body(subject: str, buckets: dict) -> str:
    bucket_html = ""
    for bucket_name, items in buckets.items():
        items_html = "".join(f"<li style='margin-bottom:6px;'>{item}</li>" for item in items)
        bucket_html += f"""
        <h3 style="color:#1a1a2e; margin-bottom:6px;">{bucket_name}</h3>
        <ul style="margin-top:0;">{items_html}</ul>
        """

    return f"""
<html><body style="font-family: Arial, sans-serif; color:#222; line-height:1.5;">
  <h2 style="color:#0b3d91;">{subject}</h2>
  {bucket_html}
  <hr style="border:none; border-top:1px solid #ddd; margin-top:20px;">
  <p style="font-size:12px; color:#888;">
    Generated by VP Daily Digest Agent · {TODAY}
  </p>
</body></html>
"""


def send_email(subject: str, html_body: str) -> None:
    if not GMAIL_PASS:
        print(f"  GMAIL_APP_PASSWORD not set — skipping: {subject}")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"VP Daily Digest <{GMAIL_USER}>"
    msg["To"] = NOTIFY_TO
    msg.attach(MIMEText(html_body, "html"))

    context = ssl.create_default_context(cafile=certifi.where())
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, NOTIFY_TO, msg.as_string())
    print(f"  Sent: {subject}")


def main():
    print(f"VP Daily Digest Agent — sending {len(EMAILS)} emails to {NOTIFY_TO} ({TODAY})")
    for email in EMAILS:
        html_body = build_html_body(email["subject"], email["buckets"])
        send_email(email["subject"], html_body)
    print("Done.")


if __name__ == "__main__":
    main()
