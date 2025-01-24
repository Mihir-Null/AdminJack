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
from Jack import (
    post_event, 
    send_email_to_list, 
    add_to_google_calendar, 
    instagram_post,
    authenticate_user,
    on_ready
)

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'client_secret.json'  # Update with your file path

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = discord.Client(intents=intents)

def open_event_details():
    def save_details():
        global description, image, instagram_access_token, instagram_user_id
        global discord_announcement_channel, server_name, channel_name
        global meeting_link, event_date, event_time, timezone

        description = desc_entry.get()
        image = image_path.get()
        instagram_access_token = insta_token_entry.get()
        instagram_user_id = insta_user_id_entry.get()
        discord_announcement_channel = discord_channel_entry.get()
        server_name = server_name_entry.get()
        channel_name = channel_name_entry.get()
        meeting_link = meeting_link_entry.get()
        event_date = event_date_entry.get()
        event_time = event_time_entry.get()
        timezone = timezone_entry.get()

        messagebox.showinfo("Success", "Event details saved!")

    details_window = tk.Toplevel(root)
    details_window.title("Enter Event Details")

    tk.Label(details_window, text="Description:").grid(row=0, column=0, sticky="e")
    desc_entry = tk.Entry(details_window, width=50)
    desc_entry.grid(row=0, column=1)

    tk.Label(details_window, text="Image Path:").grid(row=1, column=0, sticky="e")
    image_path = tk.Entry(details_window, width=50)
    image_path.grid(row=1, column=1)
    tk.Button(details_window, text="Browse", command=lambda: image_path.insert(0, filedialog.askopenfilename())).grid(row=1, column=2)

    tk.Label(details_window, text="Instagram Access Token:").grid(row=2, column=0, sticky="e")
    insta_token_entry = tk.Entry(details_window, width=50)
    insta_token_entry.grid(row=2, column=1)

    tk.Label(details_window, text="Instagram User ID:").grid(row=3, column=0, sticky="e")
    insta_user_id_entry = tk.Entry(details_window, width=50)
    insta_user_id_entry.grid(row=3, column=1)

    tk.Label(details_window, text="Discord Channel:").grid(row=4, column=0, sticky="e")
    discord_channel_entry = tk.Entry(details_window, width=50)
    discord_channel_entry.grid(row=4, column=1)

    tk.Label(details_window, text="Server Name:").grid(row=5, column=0, sticky="e")
    server_name_entry = tk.Entry(details_window, width=50)
    server_name_entry.grid(row=5, column=1)

    tk.Label(details_window, text="Channel Name:").grid(row=6, column=0, sticky="e")
    channel_name_entry = tk.Entry(details_window, width=50)
    channel_name_entry.grid(row=6, column=1)

    tk.Label(details_window, text="Meeting Link:").grid(row=7, column=0, sticky="e")
    meeting_link_entry = tk.Entry(details_window, width=50)
    meeting_link_entry.grid(row=7, column=1)

    tk.Label(details_window, text="Event Date (YYYY-MM-DD):").grid(row=8, column=0, sticky="e")
    event_date_entry = tk.Entry(details_window, width=50)
    event_date_entry.grid(row=8, column=1)

    tk.Label(details_window, text="Event Time (HH:MM):").grid(row=9, column=0, sticky="e")
    event_time_entry = tk.Entry(details_window, width=50)
    event_time_entry.grid(row=9, column=1)

    tk.Label(details_window, text="Timezone:").grid(row=10, column=0, sticky="e")
    timezone_entry = tk.Entry(details_window, width=50)
    timezone_entry.grid(row=10, column=1)

    tk.Button(details_window, text="Save", command=save_details).grid(row=11, column=1, pady=10)

def execute_action(action):
    try:
        if action == "discord":
            client.run(os.environ.get('DISCORD_BOT_TOKEN'))
            print("Posting to Discord...")
        elif action == "email":
            authenticate_user()
            send_email_to_list(description, event_date, event_time, meeting_link, "emails.csv", "email")
        elif action == "calendar":
            authenticate_user()
            add_to_google_calendar(description, event_date, event_time, timezone, meeting_link)
        elif action == "instagram":
            instagram_post(description, image)
        elif action == "all":
            # Execute all actions in sequence
            authenticate_user()
            client.run(os.environ.get('DISCORD_BOT_TOKEN'))
            print("Posting to Discord...")
            send_email_to_list(description, event_date, event_time, meeting_link, "emails.csv", "email")
            add_to_google_calendar(description, event_date, event_time, timezone, meeting_link)
            instagram_post(description, image)
        messagebox.showinfo("Success", f"Action '{action}' executed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while executing '{action}': {str(e)}")

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
