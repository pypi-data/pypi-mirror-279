from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom


async def command_botinfo(room: MatrixRoom, event: RoomMessageText, bot):
    bot.logger.log("Showing bot info...", "debug")

    body = f"""
Room info:

Bot user ID: {bot.matrix_client.user_id}
Current room ID: {room.room_id}
"""

    await bot.send_message(room, body, True)
