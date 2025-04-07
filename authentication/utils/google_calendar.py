import datetime
import os.path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def create_calendar_event(appointment):
    # Path to credentials.json
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials', 'credentials.json')

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    calendar_id = 'primary'  # or your custom calendar ID

    credentials = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)

    # Combine date and time into RFC3339 format
    start_datetime = datetime.datetime.combine(appointment.date, appointment.time)
    end_datetime = start_datetime + datetime.timedelta(minutes=30)  # assuming 30-min appointments

    event = {
        'summary': f'Appointment with {appointment.full_name}',
        'description': appointment.notes,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Africa/Nairobi',  # change to your timezone
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Africa/Nairobi',
        },
    }

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event.get('htmlLink')
