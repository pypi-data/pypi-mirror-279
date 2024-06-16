from nio import MatrixRoom, RoomMessageText

from datetime import datetime


async def message_callback(room: MatrixRoom | str, event: RoomMessageText, bot):
    bot.logger.log(f"Received message from {event.sender} in room {room.room_id}")

    sent = datetime.fromtimestamp(event.server_timestamp / 1000)
    received = datetime.now()
    latency = received - sent

    if event.sender == bot.matrix_client.user_id:
        bot.logger.log("Message is from bot itself - ignoring", "debug")

    elif event.body.startswith("!rssbot") or event.body.startswith("* !rssbot"):
        await bot.process_command(room, event)

    elif event.body.startswith("!"):
        bot.logger.log(
            f"Received {event.body} - might be a command, but not for this bot - ignoring",
            "debug",
        )

    else:
        bot.logger.log("Received regular message - ignoring", "debug")

    processed = datetime.now()
    processing_time = processed - received

    bot.logger.log(
        f"Message processing took {processing_time.total_seconds()} seconds (latency: {latency.total_seconds()} seconds)",
        "debug",
    )
