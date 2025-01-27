import google
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import smtplib
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
from datetime import datetime,timedelta
import base64

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'client_secret.json'  # Update with your file path

def authenticate_user():
    """
    Handles the OAuth flow for user authentication.
    Returns a credentials object for the user's Google account.
    """
    creds = None
    token_file = "token.json"  # File to store user tokens
    if os.path.exists(token_file):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds

def add_to_google_calendar(event_name, description, event_date, event_time, event_duration, timezone, meeting_link):
    """
    Add an event to the authenticated user's Google Calendar.
    """
    try:
        start_datetime = datetime.strptime(f"{event_date}T{event_time}:00", "%Y-%m-%dT%H:%M:%S")
        formatted_start_time = start_datetime.isoformat()

        # Add the duration to the start time
        end_datetime = start_datetime + timedelta(hours=int(event_duration))

        # Format the result back to ISO 8601
        formatted_end_time = end_datetime.isoformat()

        creds = authenticate_user()
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': event_name,
            'start': {
                'dateTime': formatted_start_time,
                'timeZone': timezone
            },
            'end': {
                'dateTime': formatted_end_time,
                'timeZone': timezone
            },
            'location': meeting_link,
            'description': description,
            'reminders': {
                'useDefault': True,
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')
        return event.get("htmlLink")

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def send_email_with_gmail_api(creds, recipient_email, subject, body):
    """
    Send an email using the Gmail API.
    """
    try:
        service = build('gmail', 'v1', credentials=creds)

        # Create the email content
        message = MIMEText(body)
        message['to'] = recipient_email
        message['from'] = "me"
        message['subject'] = subject

        # Encode the message in base64
        encoded_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        # Send the email
        send_message = service.users().messages().send(userId="me", body=encoded_message).execute()
        print(f"Email sent to {recipient_email}: {send_message['id']}")

    except HttpError as error:
        print(f"An error occurred: {error}")

def send_email_to_list(event_name, csv_file, email_column, description, event_date, event_time, meeting_link, email_checking_bool, club_name):
    """
    Read a CSV file to get a list of emails and send the event details to each.
    """
    email_list = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            if email_column not in reader.fieldnames:
                print(f"Column '{email_column}' not found in the CSV file fieldnames {reader.fieldnames}")
                return

            for row in reader:
                email = row[email_column]
                # do some basic email checking here
                if email and (email.__contains__(".com") or email.__contains__(".edu") or email.__contains__(".in") or email_checking_bool):
                    email_list.append(email)

        print(f"Emails extracted: {email_list}")

        creds = authenticate_user()
        subject = f"{club_name} Event: {event_name}"
        body_template = (
            "Hello,\n\n"
            "You are invited to the following event:\n\n"
            f"Event: {description}\n"
            f"Date: {event_date}\n"
            f"Time: {event_time}\n"
            f"Location: {meeting_link}\n\n"
            "Best regards,\n"
            f"The {club_name} team\n\n"
            f"You are recieving this email because you are on the {club_name} mailing list "
        )

        for recipient_email in email_list:
            body = body_template.format(
                description=description,
                event_date=event_date,
                event_time=event_time,
                meeting_link=meeting_link
            )
            send_email_with_gmail_api(creds, recipient_email, subject, body)

    except Exception as e:
        print(f"Failed to process the CSV file: {e}")

authenticate_user()