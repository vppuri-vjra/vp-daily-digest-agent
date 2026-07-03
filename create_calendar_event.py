#!/usr/bin/env python3
"""
VP Daily Calendar Digest-Consumption Agent

Creates exactly 1 event/day, named "Digest Consumption", on the user's Google
Calendar — a short block reserved for reading the day's digest emails/Slack
messages produced by send_digest_emails.py and send_slack_digest.py.

Auth: OAuth2 with a one-time refresh token (see get_refresh_token.py and
README.md for setup) — authenticates as the calendar owner directly, so
CALENDAR_ID is just "primary" and no calendar sharing is needed.
"""

import os
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "")
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", "")
GOOGLE_OAUTH_REFRESH_TOKEN = os.environ.get("GOOGLE_OAUTH_REFRESH_TOKEN", "")
CALENDAR_ID = os.environ.get("CALENDAR_ID", "primary")
TIMEZONE = os.environ.get("EVENT_TIMEZONE", "America/Los_Angeles")

EVENT_SUMMARY = "Digest Consumption"
EVENT_START_HOUR = 6
EVENT_START_MINUTE = 30
EVENT_DURATION_MINUTES = 15

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN_URI = "https://oauth2.googleapis.com/token"


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
    if not (GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET and GOOGLE_OAUTH_REFRESH_TOKEN):
        print("Google OAuth credentials not set — skipping calendar event creation.")
        return

    creds = Credentials(
        None,
        refresh_token=GOOGLE_OAUTH_REFRESH_TOKEN,
        client_id=GOOGLE_OAUTH_CLIENT_ID,
        client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
        token_uri=TOKEN_URI,
        scopes=SCOPES,
    )
    service = build("calendar", "v3", credentials=creds)

    event = build_event()
    print(f"Creating '{EVENT_SUMMARY}' on {CALENDAR_ID} at {event['start']['dateTime']}...")
    created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    print(f"Created: {created.get('htmlLink')}")


if __name__ == "__main__":
    main()
