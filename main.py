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
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
import json

# SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.send']
# CLIENT_SECRET_FILE = 'client_secret.json'  # Update with your file path

# # Initialize Discord client
# intents = discord.Intents.default()
# intents.message_content = True  # Enable message content intent
# client = discord.Client(intents=intents)

# File to store event details
EVENT_DETAILS_FILE = "event_details.json"

event_name = None
description = None
image = None
instagram_access_token = None
instagram_user_id = None
discord_announcement_channel = None
server_name = None
channel_name = None
meeting_link = None
event_date = None
event_time = None
timezone = None
csv_file = None
email_column = None
details = None
event_duration = 1

def save_event_details_to_file(details):
    """Save event details to a JSON file."""
    with open(EVENT_DETAILS_FILE, "w") as file:
        json.dump(details, file, indent=4)

def load_event_details_from_file():
    """Load event details from a JSON file."""
    if os.path.exists(EVENT_DETAILS_FILE):
        if os.path.getsize(EVENT_DETAILS_FILE) == 0:
            return {}
        with open(EVENT_DETAILS_FILE, "r") as file:
            return json.load(file)
    return {}

def open_event_details():
    global details
    global event_name, description, image, instagram_access_token, instagram_user_id
    global discord_announcement_channel, server_name, channel_name, meeting_link
    global event_date, event_time, timezone, csv_file, email_column
    def save_details():
        details = {
            "event_name": event_name_entry.get(),
            "description": desc_entry.get(),
            "image": image_path.get(),
            "instagram_access_token": insta_token_entry.get(),
            "instagram_user_id": insta_user_id_entry.get(),
            "discord_announcement_channel": discord_channel_entry.get(),
            "server_name": server_name_entry.get(),
            "channel_name": channel_name_entry.get(),
            "meeting_link": meeting_link_entry.get(),
            "event_date": event_date_entry.get(),
            "event_time": event_time_entry.get(),
            "timezone": timezone_entry.get(),
            "csv_file": csv_file_path.get(),
            "email_column": email_column_entry.get(),
            "event_duration": event_duration_entry.get()
        }
        
        event_name = details.get("event_name")
        description = details.get("description")
        image = details.get("image")
        instagram_access_token = details.get("instagram_access_token")
        instagram_user_id = details.get("instagram_user_id")
        discord_announcement_channel = details.get("discord_announcement_channel")
        server_name = details.get("server_name")
        channel_name = details.get("channel_name")
        meeting_link = details.get("meeting_link")
        event_date = details.get("event_date")
        event_time = details.get("event_time")
        timezone = details.get("timezone")
        csv_file = details.get("csv_file")
        email_column = details.get("email_column")
        event_duration = details.get("event_duration")        

        save_event_details_to_file(details)
        messagebox.showinfo("Success", "Event details saved!")

    # Load existing details if available
    details = load_event_details_from_file()

    event_name = details.get("event_name")
    description = details.get("description")
    image = details.get("image")
    instagram_access_token = details.get("instagram_access_token")
    instagram_user_id = details.get("instagram_user_id")
    discord_announcement_channel = details.get("discord_announcement_channel")
    server_name = details.get("server_name")
    channel_name = details.get("channel_name")
    meeting_link = details.get("meeting_link")
    event_date = details.get("event_date")
    event_time = details.get("event_time")
    timezone = details.get("timezone")
    csv_file = details.get("csv_file")
    email_column = details.get("email_column")
    event_duration = details.get("event_duration")   

    details_window = tk.Toplevel(root)
    details_window.title("Enter Event Details")

    tk.Label(details_window, text="Event name:").grid(row=0, column=0, sticky="e")
    event_name_entry = tk.Entry(details_window, width=50)
    event_name_entry.grid(row=0, column=1)
    event_name_entry.insert(0, event_name if event_name else "")

    tk.Label(details_window, text="Description:").grid(row=1, column=0, sticky="e")
    desc_entry = tk.Entry(details_window, width=50)
    desc_entry.grid(row=1, column=1)
    desc_entry.insert(0, description if description else "")

    tk.Label(details_window, text="Image Path:").grid(row=2, column=0, sticky="e")
    image_path = tk.Entry(details_window, width=50)
    image_path.grid(row=2, column=1)
    image_path.insert(0, image if image else "")
    tk.Button(details_window, text="Browse", command=lambda: image_path.insert(0, filedialog.askopenfilename())).grid(row=2, column=2)

    tk.Label(details_window, text="Instagram Access Token:").grid(row=3, column=0, sticky="e")
    insta_token_entry = tk.Entry(details_window, width=50)
    insta_token_entry.grid(row=3, column=1)
    insta_token_entry.insert(0, instagram_access_token if instagram_access_token else "")

    tk.Label(details_window, text="Instagram User ID:").grid(row=4, column=0, sticky="e")
    insta_user_id_entry = tk.Entry(details_window, width=50)
    insta_user_id_entry.grid(row=4, column=1)
    insta_user_id_entry.insert(0, instagram_user_id if instagram_user_id else "")

    tk.Label(details_window, text="Discord Channel:").grid(row=5, column=0, sticky="e")
    discord_channel_entry = tk.Entry(details_window, width=50)
    discord_channel_entry.grid(row=5, column=1)
    discord_channel_entry.insert(0, discord_announcement_channel if discord_announcement_channel else "")

    tk.Label(details_window, text="Server Name:").grid(row=6, column=0, sticky="e")
    server_name_entry = tk.Entry(details_window, width=50)
    server_name_entry.grid(row=6, column=1)
    server_name_entry.insert(0, server_name if server_name else "")

    tk.Label(details_window, text="Channel Name:").grid(row=7, column=0, sticky="e")
    channel_name_entry = tk.Entry(details_window, width=50)
    channel_name_entry.grid(row=7, column=1)
    channel_name_entry.insert(0, channel_name if channel_name else "")

    tk.Label(details_window, text="Meeting Link:").grid(row=8, column=0, sticky="e")
    meeting_link_entry = tk.Entry(details_window, width=50)
    meeting_link_entry.grid(row=8, column=1)
    meeting_link_entry.insert(0, meeting_link if meeting_link else "")

    tk.Label(details_window, text="Event Date (YYYY-MM-DD):").grid(row=9, column=0, sticky="e")
    event_date_entry = tk.Entry(details_window, width=50)
    event_date_entry.grid(row=9, column=1)
    event_date_entry.insert(0, event_date if event_date else "")

    tk.Label(details_window, text="Event Time (HH:MM):").grid(row=10, column=0, sticky="e")
    event_time_entry = tk.Entry(details_window, width=50)
    event_time_entry.grid(row=10, column=1)
    event_time_entry.insert(0, event_time if event_time else "")

    tk.Label(details_window, text="Timezone:").grid(row=11, column=0, sticky="e")
    timezone_entry = tk.Entry(details_window, width=50)
    timezone_entry.grid(row=11, column=1)
    timezone_entry.insert(0, timezone if timezone else "")

    tk.Label(details_window, text="Email CSV Path:").grid(row=12, column=0, sticky="e")
    csv_file_path = tk.Entry(details_window, width=50)
    csv_file_path.grid(row=12, column=1)
    csv_file_path.insert(0, csv_file if csv_file else "")
    tk.Button(details_window, text="Browse", command=lambda: csv_file_path.insert(0, filedialog.askopenfilename())).grid(row=12, column=2)

    tk.Label(details_window, text="Email Column:").grid(row=13, column=0, sticky="e")
    email_column_entry = tk.Entry(details_window, width=50)
    email_column_entry.grid(row=13, column=1)
    email_column_entry.insert(0, email_column if email_column else "")

    tk.Label(details_window, text="Event Duration:").grid(row=14, column=0, sticky="e")
    event_duration_entry = tk.Entry(details_window, width=50)
    event_duration_entry.grid(row=14, column=1)
    event_duration_entry.insert(0, event_duration if event_duration else "")

    tk.Button(details_window, text="Save", command=save_details).grid(row=15, column=1, pady=10)

def execute_action(action):
    global event_name, description, image, instagram_access_token, instagram_user_id
    global discord_announcement_channel, server_name, channel_name, meeting_link
    global event_date, event_time, timezone, csv_file, email_column
    try:
        if action == "discord":
            print("Posting to Discord...")
            import Jack_Discord
            from Jack_Discord import call_post_event
            call_post_event(description, image, channel_name, event_name, meeting_link, server_name,event_date,event_time, event_duration)
        elif action == "email":
            import Jack_Google
            from Jack_Google import send_email_to_list
            send_email_to_list()
        elif action == "calendar":
            import Jack_Google
            from Jack_Google import add_to_google_calendar
            add_to_google_calendar()
        elif action == "instagram":
            import Jack_Insta
            from Jack_Insta import instagram_post
            instagram_post()
        elif action == "all":
            print("Posting to Discord...")
            import Jack_Discord
            from Jack_Discord import call_post_event
            call_post_event(description, image, channel_name, event_name, meeting_link, server_name,event_date,event_time, event_duration)
            import Jack_Google
            from Jack_Google import send_email_to_list,add_to_google_calendar
            send_email_to_list()
            add_to_google_calendar()
            import Jack_Insta
            from Jack_Insta import instagram_post
            instagram_post()
        
        messagebox.showinfo("Success", f"Action '{action}' executed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while executing 6{action}': {str(e)}")

root = tk.Tk()
root.title("Event Post Bot")

# Main screen
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

buttons = [
    ("Post to Discord", "discord"),
    ("Send Emails", "email"),
    ("Add to Calendar", "calendar"),
    ("Post to Instagram", "instagram"),
    ("Execute All", "all")
]

for i, (label, action) in enumerate(buttons):
    tk.Button(main_frame, text=label, width=20, command=lambda act=action: execute_action(act)).grid(row=i, column=0, pady=5)

# Event details button
tk.Button(root, text="Enter Event Details", command=open_event_details, width=25).pack(pady=20)

root.mainloop()
