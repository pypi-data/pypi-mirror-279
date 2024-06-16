from nio.events.room_events import RoomMessageText
from nio.rooms import MatrixRoom


async def command_eventtype(room: MatrixRoom, event: RoomMessageText, bot):
    if len(event.body.split()) < 3:
        # Return the room's current event type
        state = bot.get_event_type_for_room(room)
        await bot.send_message(room, f"The current event type for this room is {state}.", True)

    elif len(event.body.split()) == 3:
        if event.body.split()[2] in ("text", "notice"):
            # Set the room's event type
            await bot.set_event_type_for_room(room, event.body.split()[2])
            await bot.send_message(room, f"Event type for this room set to {event.body.split()[2]}.", True)

        else:
            await bot.send_message(room, "Invalid event type. Valid event types are 'text' and 'notice'.", True)

    else:
        await bot.send_message(room, "Invalid syntax. Usage: !rssbot eventtype [text|notice]", True)