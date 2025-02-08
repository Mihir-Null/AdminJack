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
## Instagram 
To post to Instagram using the Instagram Graph API, you need the following credentials:  

- **Instagram Access Token** (`INSTAGRAM_ACCESS_TOKEN`)  
- **Instagram User ID** (`INSTAGRAM_USER_ID`)  

### **Step 1: Set Up a Meta (Facebook) App**
1. **Go to the [Meta Developer Portal](https://developers.facebook.com/)**.  
2. Click **"Get Started"** and follow the on-screen instructions if you haven't already set up a developer account.  
3. Go to **"My Apps"** → Click **"Create App"**.  
4. Select **"Business"** and click **"Continue"**.  
5. Enter the app name, contact email, and create the app.  

---

### **Step 2: Add Instagram API to Your App**
1. Inside your newly created app, go to **"Add a Product"** → Select **"Instagram Graph API"** → Click **"Set Up"**.  
2. In the left panel, go to **"Settings" → "Basic"**.  
3. Scroll down to **"Add Platform"** → Select **"Website"** and enter your website URL (use any if testing).  

---

### **Step 3: Create an Instagram Business/Creator Account**
1. Go to [Instagram](https://www.instagram.com/) and log in.  
2. Click **Profile** → **Edit Profile**.  
3. Under **"Professional Account"**, ensure your account is set to **Business or Creator**.  
4. **Link your Instagram account** to a **Facebook Page** (this is mandatory).  
   - Go to **Facebook Business Suite** → **Business Settings** → **Accounts → Instagram Accounts** → **Add Account**.  

---

### **Step 4: Generate a User Access Token**
1. **Go to the [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)**.  
2. Select your App from the dropdown.  
3. Under **Permissions**, add the following:  
   ```
   instagram_basic, instagram_content_publish
   ```
4. Click **"Generate Access Token"** and approve the request.  
5. **Copy the Access Token** (`INSTAGRAM_ACCESS_TOKEN`).  

---

### **Step 5: Get Your Instagram User ID**
1. Open a new browser tab and enter the following request in the [Graph API Explorer](https://developers.facebook.com/tools/explorer/):  
   ```
   https://graph.facebook.com/v15.0/me?fields=id,username&access_token=YOUR_ACCESS_TOKEN
   ```
2. Click **Submit**.  
3. The response will contain your Instagram **User ID** (`INSTAGRAM_USER_ID`).  

---

### **Step 6: Store Credentials in the `.env` File**
Create or edit the `.env` file and store the credentials securely:  

```
INSTAGRAM_ACCESS_TOKEN=your-access-token-here
INSTAGRAM_USER_ID=your-user-id-here
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
