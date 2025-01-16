# AdminJack
One click administration for interest clubs

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
 - go through discord bot oauth2 and authorize events
 - fix formatting and integration on discord
 - might want to add some way for discord admins to authorize the announcement when we need the same bot to work in multiple servers
 - add default messages for each platform to add at the end
 - test and fix gmail formatting, and all other formatting
 - add cross integration between all platforms (messages have calendar event, etc.)
 - instagram posting
 - listserv emailing with special message
