import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import google
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox, filedialog
import json
from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
import base64

# File to store event details
EVENT_DETAILS_FILE = "event_details.json"
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'client_secret.json'  # Update with your file path

def save_event_details_to_file(details):
    """Save event details to a JSON file."""
    with open(EVENT_DETAILS_FILE, "w") as file:
        json.dump(details, file, indent=4)

def load_event_details_from_file():
    """Load event details from a JSON file and ensure correct data types."""
    if os.path.exists(EVENT_DETAILS_FILE) and os.path.getsize(EVENT_DETAILS_FILE) > 0:
        with open(EVENT_DETAILS_FILE, "r") as file:
            details = json.load(file)
    else:
        details = {}
    
    # Ensure proper types for numerical fields
    details["event_duration"] = int(details.get("event_duration", 1))
    
    return details

def authenticate_user():
    creds = None
    token_file = "token.json"
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def add_to_google_calendar(details):
    try:
        start_datetime = datetime.strptime(f"{details['event_date']}T{details['event_time']}:00", "%Y-%m-%dT%H:%M:%S")
        formatted_start_time = start_datetime.isoformat()
        end_datetime = start_datetime + timedelta(hours=int(details['event_duration']))
        formatted_end_time = end_datetime.isoformat()

        creds = authenticate_user()
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary': details['event_name'],
            'start': {'dateTime': formatted_start_time, 'timeZone': details['timezone']},
            'end': {'dateTime': formatted_end_time, 'timeZone': details['timezone']},
            'location': details['meeting_link'],
            'description': details['description'],
            'reminders': {'useDefault': True},
        }
        
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')
        return event.get("htmlLink")
    
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def send_email_with_gmail_api(creds, recipient_email, subject, body):
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(body)
        message['to'] = recipient_email
        message['from'] = "me"
        message['subject'] = subject
        encoded_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        send_message = service.users().messages().send(userId="me", body=encoded_message).execute()
        print(f"Email sent to {recipient_email}: {send_message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def send_email_to_list(details):
    email_list = []
    try:
        with open(details['csv_file'], mode='r') as file:
            reader = csv.DictReader(file)
            if details['email_column'] not in reader.fieldnames:
                print(f"Column '{details['email_column']}' not found in CSV file fieldnames {reader.fieldnames}")
                return
            for row in reader:
                email = row[details['email_column']]
                if email and (email.__contains__(".com") or email.__contains__(".edu") or email.__contains__(".in") or details['email_checking_bool']):
                    email_list.append(email)
        print(f"Emails extracted: {email_list}")
        creds = authenticate_user()
        subject = f"{details['club_name']} Event: {details['event_name']}"
        body_template = (
            "Hello,\n\n"
            "You are invited to the following event:\n\n"
            f"Event: {details['description']}\n"
            f"Date: {details['event_date']}\n"
            f"Time: {details['event_time']}\n"
            f"Location: {details['meeting_link']}\n\n"
            "Best regards,\n"
            f"The {details['club_name']} team\n\n"
            f"You are receiving this email because you are on the {details['club_name']} mailing list "
        )
        for recipient_email in email_list:
            body = body_template
            send_email_with_gmail_api(creds, recipient_email, subject, body)
    except Exception as e:
        print(f"Failed to process the CSV file: {e}")

def send_custom_emails(details, email_names):
    creds = authenticate_user()
    emails_dict = {
        " e.g listserv request" :
        (
            f"recipient_email",
            f"custom subject",
            f"custom body"
        )

    }
    for email in email_names:
        recipient_email, subject, body = emails_dict[email]
        send_email_with_gmail_api(creds, recipient_email, subject, body)
authenticate_user()
