import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import timedelta,date,datetime,timezone
from zoneinfo import ZoneInfo 
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = discord.Client(intents=intents)


#comments are for wussie
def call_post_event(description, image, channel_name, event_name, meeting_link, server_name, event_date,event_time,event_timezone, event_duration=1):
    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")
        await post_event(description, image, channel_name, event_name, meeting_link, server_name, event_date,event_time,event_timezone, event_duration)
        await client.close()
    
    client.run(os.environ.get('DISCORD_BOT_TOKEN'))


# will want to modify this later https://discordjs.guide/popular-topics/embeds.html#using-an-embed-object
async def post_event(description, image, channel_name, event_name, meeting_link, server_name, event_date,event_time,event_timezone, event_duration=1):
    # Debug: Print guild information
    for guild in client.guilds:
        print(f"Bot is in guild: {guild.name} (ID: {guild.id})")
    print(f"Server name: {server_name}")

    # Get the guild and channel
    guild = discord.utils.get(client.guilds, name=server_name)
    if guild is None:
        print("Could not find the target guild. Please check the guild name.")
        await client.close()
        return

    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel is None:
        print("Could not find the target channel. Please check the channel name.")
        await client.close()
        return

    try:
        # Parse the event date and time
        event_start_time = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo(event_timezone))
        event_end_time = event_start_time + timedelta(hours=event_duration)

        created_event = await guild.create_scheduled_event(
            name=event_name,
            start_time=event_start_time,
            end_time=event_end_time,
            location=meeting_link,
            description=description,
            entity_type=discord.EntityType.external,  # External event type
            privacy_level=discord.PrivacyLevel.guild_only  # Correct privacy level
        )

        print(f"Discord event created: {created_event.url}")

        # Announce the event in the specified channel
        embed = discord.Embed(title=event_name, description=(description + "\n@everyone"), color=0x00ff00)
        embed.add_field(name="Event Link", value=created_event.url, inline=True)
        embed.set_image(url=f"attachment://event_image.png")

        with open(image, "rb") as img_file:
            discord_file = discord.File(img_file, filename="event_image.png")
            await channel.send(file=discord_file, embed=embed)

        print("Event announced to Discord successfully!")

    except Exception as e:
        print(f"Failed to create or announce the event: {e}")

    finally:
        # Close the client after posting the event
        await client.close()





    


#client.run(os.environ.get('DISCORD_BOT_TOKEN'))
