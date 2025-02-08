# AdminJack
One click administration for interest clubs

# Setup and Authentication Keys
## Google
The Google endpoints for AdminJack rely on a Google Cloud App. The safest way to route your information for this is to create your own Google Cloud App for your club's use.
To obtain the `client_secret` for your Google Cloud app, follow these steps:

### **1. Create or Select a Google Cloud Project**
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Select an existing project or create a new one.
- Go to the OAuth Consent screen (or when prompted to) Edit the App Registration
- When asked to add scopes enter the list below:
  - https://www.googleapis.com/auth/calendar.app.created
  - https://www.googleapis.com/auth/calendar.calendarlist.readonly
  - https://www.googleapis.com/auth/calendar.events.freebusy
  - https://www.googleapis.com/auth/calendar.events.public.readonly
  - https://www.googleapis.com/auth/calendar.settings.readonly
  - https://www.googleapis.com/auth/calendar.freebusy
  - https://www.googleapis.com/auth/gmail.send
  - https://www.googleapis.com/auth/calendar.readonly
  - https://www.googleapis.com/auth/calendar.calendars
  - https://www.googleapis.com/auth/calendar.calendars.readonly
  - https://www.googleapis.com/auth/calendar.events
  - https://www.googleapis.com/auth/calendar.events.owned
  - https://www.googleapis.com/auth/calendar.events.owned.readonly
  - https://www.googleapis.com/auth/calendar.events.readonly
- When prompted to enter Test users add the email address you intend to use for the club

### **2. Enable OAuth 2.0 for Your App**
- Navigate to **APIs & Services** > **Credentials**.
- Click **Create Credentials** > **OAuth 2.0 Client ID**.

### **3. Configure OAuth Consent Screen**
- If you haven't already set it up, you’ll be prompted to configure the OAuth consent screen.
- Choose **External** (for public use) or **Internal** (for Google Workspace users in your org).
- Fill in the required details, including scopes and authorized domains.

### **4. Generate Client ID and Secret**
- Under **Credentials**, click **Create Credentials** > **OAuth Client ID**.
- Choose **Desktop App** as your app type:
- Configure **Authorized Redirect URIs** if you want to.
- Click **Create** to generate the credentials.

### **5. Download Your Client Secret**
- A dialog box will show the **Client ID** and **Client Secret**.
- Click **Download JSON** to save your credentials (this includes `client_secret`).

### **6. Store It in the AdminJack Folder**
- Store your credentials in the same folder as the AdminJack python scripts. **Guard this secret file closely**

## Discord
### **How to Create a Discord Bot and Store Its Credentials in a `.env` File**

#### **Step 1: Create a Discord Application**
1. **Go to the Discord Developer Portal**:  
   - Visit [Discord Developer Portal](https://discord.com/developers/applications).
   - Log in with your Discord account.

2. **Create a New Application**:  
   - Click **"New Application"**.
   - Give your bot a name (e.g., `Administrator Jack`).
   - Click **"Create"**.

#### **Step 2: Create a Bot User**
1. **Go to the "Bot" Section**:  
   - In the left menu, select **"Bot"**.
   - Click **"Add Bot"**, then confirm by clicking **"Yes, do it!"**.

2. **Configure the Bot**:  
   - Set an **Avatar (optional)**.
   - Toggle **"Public Bot"** off if you don’t want others adding the bot.
   - Enable **"Presence Intent"** and **"Server Members Intent"** (for mentioning users).
   - Copy the **Token** (you will need this in `.env`).

#### **Step 3: Assign Required Permissions**
1. **Go to "OAuth2" → "URL Generator"**:
   - Select **"Bot"** as a scope.
   - Under "Bot Permissions," select:
   - ![image](https://github.com/user-attachments/assets/835d553f-8550-4b83-9b59-d7e41ccb6bcc)
   - You can also just give it Administrator permissions or all permissions but I'm not responsible if it goes rogue.
   - Copy the generated URL.

2. **Invite the Bot to Your Server**:  
   - Paste the copied URL into your browser.
   - Select your server and authorize.

#### **Step 4: Store Credentials in a `.env` File**
1. **Create a `.env` File** in Your Project Directory.
2. **Store the Bot Token Securely**:
   ```
   DISCORD_TOKEN=your-bot-token-here
   ```

# Usage
## Fields
## Functions
## Custom Emails

# Intended Feature list
- Inputs
  - event description
  - image
  - various API keys
- Output Points
  - Instagram Posts (via graph API)
  - Google calendar endpoints
  - discord bot integration/announcements
  - automatic relay emailing -> gmail integration/roundcube integration -> maybe terplink integration?
    - automatic emailing for newsletters and room booking
  - automatic zoom recording uploading and sharing
  - selenium room booking, might also have to be used for terplink
  - automatic contacting of speakers?
  - automatic poster creation by prefilling fields -> could maybe do this by AI editing pdfs
  - linkedin posting if I have the time

## ToDo
- add default messages for each platform to add at the end (check from existing emails/announcements)
- specific emails to different people/ different automatic emails in formats
- fix event formatting on discord and general formatting everywhere
- add cross integration between all platforms (messages have calendar event, etc.)
- add mechanism to add to specific calendars
- canva automation
- might want to add some way for discord admins to authorize the announcement when we need the same bot to work in multiple servers
