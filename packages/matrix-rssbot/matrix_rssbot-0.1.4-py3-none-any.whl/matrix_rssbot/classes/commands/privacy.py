from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom


async def command_privacy(room: MatrixRoom, event: RoomMessageText, bot):
    body = "**Privacy**\n\nIf you use this bot, note that your messages will be sent to the following recipients:\n\n"

    body += (
        "- The bot's operator" + (f"({bot.operator})" if bot.operator else "") + "\n"
    )
    body += "- The operator(s) of the involved Matrix homeservers\n"

    await bot.send_message(room, body, True)
