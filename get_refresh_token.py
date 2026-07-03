#!/usr/bin/env python3
"""
One-time helper: run this LOCALLY (never in CI) to get a Google OAuth refresh
token for the Calendar agent (create_calendar_event.py).

Usage:
  1. Fill in GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET in .env
     (from a Desktop-app OAuth client in Google Cloud Console — see README.md).
  2. Run: python3 get_refresh_token.py
  3. A browser opens — sign in as vp.puri@gmail.com and grant calendar access.
  4. The refresh token is printed. Put it in .env / GitHub secrets as
     GOOGLE_OAUTH_REFRESH_TOKEN. Do not paste it into a chat conversation.
"""

import os

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", "")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

CLIENT_CONFIG = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }
}


def main():
    if not (CLIENT_ID and CLIENT_SECRET):
        raise SystemExit("Set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET in .env first.")

    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")

    print("\nSuccess. Add this to .env / GitHub secrets as GOOGLE_OAUTH_REFRESH_TOKEN:\n")
    print(creds.refresh_token)


if __name__ == "__main__":
    main()
