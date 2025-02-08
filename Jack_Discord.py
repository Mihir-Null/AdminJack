import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import timedelta,date,datetime,timezone
from zoneinfo import ZoneInfo
import json
load_dotenv()

# File to store event details
EVENT_DETAILS_FILE = "event_details.json"

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

def call_post_event(details):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")
        await post_event(details, client)
        await client.close()
    
    client.run(os.environ.get('DISCORD_BOT_TOKEN'))

async def post_event(details, client):
    for guild in client.guilds:
        print(f"Bot is in guild: {guild.name} (ID: {guild.id})")
    print(f"Server name: {details['server_name']}")

    guild = discord.utils.get(client.guilds, name=details['server_name'])
    if guild is None:
        print("Could not find the target guild. Please check the guild name.")
        await client.close()
        return

    channel = discord.utils.get(guild.channels, name=details['channel_name'])
    if channel is None:
        print("Could not find the target channel. Please check the channel name.")
        await client.close()
        return

    try:
        event_start_time = datetime.strptime(f"{details['event_date']} {details['event_time']}", "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo(details['timezone']))
        event_end_time = event_start_time + timedelta(hours=details['event_duration'])

        created_event = await guild.create_scheduled_event(
            name=details['event_name'],
            start_time=event_start_time,
            end_time=event_end_time,
            location=details['meeting_link'],
            description=details['description'],
            entity_type=discord.EntityType.external,
            privacy_level=discord.PrivacyLevel.guild_only
        )

        print(f"Discord event created: {created_event.url}")
        desc=(
            "**" + details['event_name'] + "**" 
            + "\n" + details['description']
            + "\n" 
            + "\nLocation/Link: " + details['meeting_link']
            + "\nDate: " + event_start_time.strftime("%B %d, %Y")
            + "\nTime: " + event_start_time.strftime("%I:%M %p %Z")
            + "\n"
            + "\n@everyone")
        embed = discord.Embed(
            title=details['event_name'], 
            #description=desc,
            color=0x00ff00)
        embed.add_field(name="Discord Event Link", value=created_event.url, inline=True)
        embed.set_image(url=f"attachment://event_image.png")

        with open(details['image'], "rb") as img_file:
            discord_file = discord.File(img_file, filename="event_image.png")
            await channel.send(desc)
            await channel.send(file=discord_file, embed=embed)

        print("Event announced to Discord successfully!")

    except Exception as e:
        print(f"Failed to create or announce the event: {e}")
    
    finally:
        await client.close()

