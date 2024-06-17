from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom

async def command_listfeeds(room: MatrixRoom, event: RoomMessageText, bot):
    state = await bot.get_state_event(room, "rssbot.feeds")

    if (not state) or (not state["content"]["feeds"]):
        message = "There are currently no feeds associated with this room."
    else:
        message = "This room is currently bridged to the following feeds:\n\n"

        for key, value in enumerate(state["content"]["feeds"]):
            message += f"- {key}: {value}\n"

    await bot.send_message(room, message, True)