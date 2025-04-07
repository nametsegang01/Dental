import datetime
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
BASE_DIR = settings.BASE_DIR

# Path to your credentials
GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials', 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_calendar_event(appointment):
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': f'Appointment: {appointment.full_name}',
        'description': appointment.notes or "No notes provided",
        'start': {
            'dateTime': datetime.datetime.combine(
                appointment.date, appointment.time
            ).isoformat(),
            'timeZone': 'Africa/Nairobi',  # Replace with your timezone
        },
        'end': {
            'dateTime': (
                datetime.datetime.combine(appointment.date, appointment.time)
                + datetime.timedelta(minutes=30)
            ).isoformat(),
            'timeZone': 'Africa/Nairobi',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('htmlLink')
