from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom

async def command_removefeed(room: MatrixRoom, event: RoomMessageText, bot):
    identifier = event.body.split()[2]

    state = await bot.get_state_event(room, "rssbot.feeds")

    if (not state) or (not state["content"]["feeds"]):
        feeds = []
    else:
        feeds = state["content"]["feeds"]
        
    if identifier.isnumeric():
        try:
            feeds.pop(int(identifier))
        except IndexError:
            await bot.send_message(room, f"There is no feed with index {identifier}.")
            return
    else:
        try:
            feeds.remove(identifier)
        except ValueError:
            await bot.send_message(room, "There is no bridged feed with the provided URL.")
            return

    await bot.send_state_event(room, "rssbot.feeds", {"feeds": feeds})