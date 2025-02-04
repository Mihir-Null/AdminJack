import os
from dotenv import load_dotenv
import requests
load_dotenv()

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

def instagram_post(details):
    """
    Post an image and description to Instagram using the Instagram Graph API.
    """
    try:
        instagram_access_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
        instagram_user_id = os.environ.get("INSTAGRAM_USER_ID")
        
        # Step 1: Upload the image
        image_upload_url = f"https://graph.facebook.com/v15.0/{instagram_user_id}/media"
        image_payload = {
            "image_url": f"{os.path.abspath(details['image'])}",
            "caption": details['description'],
            "access_token": instagram_access_token
        }
        image_response = requests.post(image_upload_url, data=image_payload)
        image_response_data = image_response.json()

        if "id" not in image_response_data:
            print(f"Error uploading image to Instagram: {image_response_data}")
            return

        creation_id = image_response_data["id"]

        # Step 2: Publish the uploaded image
        publish_url = f"https://graph.facebook.com/v15.0/{instagram_user_id}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": instagram_access_token
        }
        publish_response = requests.post(publish_url, data=publish_payload)
        publish_response_data = publish_response.json()

        if "id" not in publish_response_data:
            print(f"Error publishing post on Instagram: {publish_response_data}")
            return

        print("Post successfully published on Instagram!")

    except Exception as e:
        print(f"An error occurred while posting to Instagram: {e}")
