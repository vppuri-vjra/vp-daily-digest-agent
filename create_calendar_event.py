#!/usr/bin/env python3
"""
VP Daily Calendar Digest-Consumption Agent

Creates exactly 1 event/day, named "Digest Consumption", on the target Google
Calendar — a short block reserved for reading the day's digest emails/Slack
messages produced by send_digest_emails.py and send_slack_digest.py.

Auth: a Google service account with the Calendar API enabled, and the target
calendar shared with the service account's email (Settings > Share with
specific people > "Make changes to events"). See README.md for setup steps.
"""

import json
import os
from datetime import datetime, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
CALENDAR_ID = os.environ.get("CALENDAR_ID", "vp.puri@gmail.com")
TIMEZONE = os.environ.get("EVENT_TIMEZONE", "America/Los_Angeles")

EVENT_SUMMARY = "Digest Consumption"
EVENT_START_HOUR = 6
EVENT_START_MINUTE = 30
EVENT_DURATION_MINUTES = 15

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def build_event() -> dict:
    today = datetime.now().date()
    start = datetime.combine(today, datetime.min.time()).replace(
        hour=EVENT_START_HOUR, minute=EVENT_START_MINUTE
    )
    end = start + timedelta(minutes=EVENT_DURATION_MINUTES)

    return {
        "summary": EVENT_SUMMARY,
        "description": (
            "Time to review today's digest emails and #engg-2pm-in Slack messages: "
            "Decisions needed, Deadlines, Blockers, Required actions."
        ),
        "start": {"dateTime": start.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end.isoformat(), "timeZone": TIMEZONE},
    }


def main():
    if not GOOGLE_SERVICE_ACCOUNT_JSON:
        print("GOOGLE_SERVICE_ACCOUNT_JSON not set — skipping calendar event creation.")
        return

    info = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    service = build("calendar", "v3", credentials=creds)

    event = build_event()
    print(f"Creating '{EVENT_SUMMARY}' on {CALENDAR_ID} at {event['start']['dateTime']}...")
    created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    print(f"Created: {created.get('htmlLink')}")


if __name__ == "__main__":
    main()
