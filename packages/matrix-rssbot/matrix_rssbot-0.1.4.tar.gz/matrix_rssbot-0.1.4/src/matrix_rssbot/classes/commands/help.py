from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom


async def command_help(room: MatrixRoom, event: RoomMessageText, bot):
    body = """Available commands:

- !rssbot help - Show this message
- !rssbot botinfo - Show information about the bot
- !rssbot privacy - Show privacy information
- !rssbot addfeed \<url\> - Bridges a new feed to the current room
- !rssbot listfeeds - Lists all bridged feeds
- !rssbot removefeed \<index|url\> - Removes a bridged feed given the numeric index from the listfeeds command or the URL of the feed
- !rssbot eventtype [text|notice] - Sets the event type for the current room, overriding the default event type
"""

    await bot.send_message(room, body, True)
