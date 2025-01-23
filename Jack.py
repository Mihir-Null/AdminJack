import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
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

club_name = ""
event_name = ""
description = "testing event description"
image = "event_image.png" # file path
discord_announcement_channel = ""
server_name = "random vids and tests"
channel_name = "dab"
meeting_link = ""
event_date = "2025-01-17"
event_time = "14:30"
event_duration = 1
timezone = "America/New_York"
email_file = "Roster.csv"
email_column = "Campus Email"
email_checking_bool = False

# Replace 'YOUR_CHANNEL_ID' with the channel ID where you want the bot to post
channel_id = "announcements"

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = discord.Client(intents=intents)

# need to add adding a discord event automagically as well
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await post_event(description=description, image=image, channel_name=channel_name)
    await client.close()


# will want to modify this later https://discordjs.guide/popular-topics/embeds.html#using-an-embed-object
async def post_event(description: str, image, channel_name):
    guild = discord.utils.get(client.guilds, name=server_name)  # Replace 'Your Guild Name' with the actual guild name
    if guild is None:
        print("Could not find the target guild. Please check the guild name.")
        return
    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel is None:
        print("Could not find the target channel. Please check the channel ID.")
        return

    try:
        # Create a scheduled event in the guild
        event_start_time = discord.utils.utcnow()
        event_end_time = event_start_time + discord.utils.timedelta(hours=event_duration)  # 1-hour event duration

        created_event = await guild.create_scheduled_event(
            name=event_name,
            start_time=event_start_time,
            end_time=event_end_time,
            location=meeting_link,
            description=description,
        )

        print(f"Discord event created: {created_event.url}")

        # Announce the event in the specified channel
        embed = discord.Embed(title=event_name, description=(description + "\n@everyone"), color=0x00ff00)
        embed.add_field(name="Event Link", value=created_event.url, inline=True)
        embed.set_image(url=f"attachment://event_image.png")

        with open(image, "rb") as img_file:
            discord_file = discord.File(img_file, filename="event_image.png")
            await channel.send(file=discord_file, embed=embed)

        print("Event announced to discord successfully!")

    except Exception as e:
        print(f"Failed to create or announce the event: {e}")

client.run(os.environ.get('DISCORD_BOT_TOKEN'))

# Google Calendar Section

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

def add_to_google_calendar(event_description, event_date, event_time, timezone, meeting_link):
    """
    Add an event to the authenticated user's Google Calendar.
    """
    try:
        creds = authenticate_user()
        service = build('calendar', 'v3', credentials=creds)

        event = {
            'summary': event_name,
            'start': {
                'dateTime': f'{event_date}T{event_time}:00',
                'timeZone': timezone
            },
            'end': {
                'dateTime': f'{event_date}T{event_time}:00',
                'timeZone': timezone
            },
            'location': meeting_link,
            'description': event_description,
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

print("flag1")
authenticate_user()
print("flag2")
add_to_google_calendar(event_description=description, event_date=event_date, event_time=event_time, timezone=timezone, meeting_link=meeting_link)

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

def send_email_to_list(event_description, event_date, event_time, meeting_link, csv_file, email_column):
    """
    Read a CSV file to get a list of emails and send the event details to each.
    """
    email_list = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            if email_column not in reader.fieldnames:
                print(f"Column '{email_column}' not found in the CSV file.")
                return

            for row in reader:
                email = row[email_column]
                # do some basic email checking here
                if email and (email.__contains__(".com") or email.__contains__(".edu") or email.__contains__(".in") or email_checking_bool):
                    email_list.append(email)

        print(f"Emails extracted: {email_list}")

        creds = authenticate_user()
        subject = "{club_name} Event: {event_name}"
        body_template = (
            "Hello,\n\n"
            "You are invited to the following event:\n\n"
            "Event: {event_description}\n"
            "Date: {event_date}\n"
            "Time: {event_time}\n"
            "Link: {meeting_link}\n\n"
            "Best regards,\n"
            "The {club_name} team\n\n"
            "You are recieving this email because you are on the {club_name} mailing list "
        )

        for recipient_email in email_list:
            body = body_template.format(
                event_description=event_description,
                event_date=event_date,
                event_time=event_time,
                meeting_link=meeting_link
            )
            send_email_with_gmail_api(creds, recipient_email, subject, body)

    except Exception as e:
        print(f"Failed to process the CSV file: {e}")

def instagram_post(){
    
}