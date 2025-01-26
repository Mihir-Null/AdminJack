import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = discord.Client(intents=intents)

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

#comments are for wussie
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await post_event()
    await client.close()


# will want to modify this later https://discordjs.guide/popular-topics/embeds.html#using-an-embed-object
async def post_event(description=description, image=image, channel_name=channel_name, event_name = event_name, event_duration=event_duration, meeting_link=meeting_link, server_name = server_name):
    #debug
    for guild in bot.guilds:
        print(f"Bot is in guild: {guild.name} (ID: {guild.id})")
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

def init_bot_details(description=description, image=image, channel_name=channel_name, event_name = event_name, event_duration=event_duration, meeting_link=meeting_link, server_name=server_name):
    description = description
    image = image
    channel_name = channel_name
    event_name = event_name
    event_duration = event_duration
    meeting_link = meeting_link
    server_name = server_name


print("posting to Discord")
#client.run(os.environ.get('DISCORD_BOT_TOKEN'))
