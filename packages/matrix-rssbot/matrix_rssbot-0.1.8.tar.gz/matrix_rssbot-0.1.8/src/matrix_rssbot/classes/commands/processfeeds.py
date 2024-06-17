from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom

async def command_processfeeds(room: MatrixRoom, event: RoomMessageText, bot):
    bot.logger.log(f"Processing feeds for room {room.room_id}")

    await bot.process_room(room)