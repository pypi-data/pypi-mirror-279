from nio.events.room_events import RoomMessageText
from nio import RoomPutStateError
from nio.rooms import MatrixRoom

from datetime import datetime

import feedparser


async def command_addfeed(room: MatrixRoom, event: RoomMessageText, bot):
    args = event.body.split()[2:]

    if not args:
        await bot.send_message(room, "Please provide a feed URL to add.", True)
        return

    if "--backfill" in args:
        backfill = True
        args.remove("--backfill")

    else:
        backfill = False

    if len(args) != 1:
        await bot.send_message(room, "Please provide only one feed URL.", True)
        return

    url = args[0]

    bot.logger.log(f"Adding new feed to room {room.room_id}")

    state = await bot.get_state_event(room, "rssbot.feeds")

    if not state:
        feeds = []
    else:
        feeds = state["content"]["feeds"]

    feeds.append(url)

    feeds = list(set(feeds))

    try:
        feedparser.parse(url)
    except Exception as e:
        await bot.send_state_event(
            f"Could not access or parse feed at {url}. Please ensure that you got the URL right, and that it is actually an RSS/Atom feed.",
            True,
        )
        bot.logger.log(f"Could not access or parse feed at {url}: {e}", "error")

    try:
        response1 = await bot.send_state_event(
            room,
            "rssbot.feed_state",
            {"timestamp": int(datetime.now().timestamp())},
            url,
        )

        if isinstance(response1, RoomPutStateError):
            if response1.status_code == "M_FORBIDDEN":
                await bot.send_message(
                    room,
                    "Unable to put status events into this room. Please ensure I have the required permissions, then try again.",
                )

            await bot.send_message(
                room, "Unable to write feed state to the room. Please try again.", True
            )
            bot.logger.log(
                f"Error adding feed to room {room.room_id}: {response1.error}", "error"
            )
            return

        response2 = await bot.send_state_event(room, "rssbot.feeds", {"feeds": feeds})

        if isinstance(response2, RoomPutStateError):
            await bot.send_message(
                room, "Unable to write feed list to the room. Please try again.", True
            )
            bot.logger.log(
                f"Error adding feed to room {room.room_id}: {response2.error}", "error"
            )
            return

        await bot.send_message(room, f"Added {url} to this room's feeds.", True)

        if backfill:
            await bot.send_message(
                room,
                "Backfilling messages from the feed. This may take a while, depending on the feed size.",
                True,
            )

            await bot.backfill_feed(room, url)

    except Exception as e:
        await bot.send_message(
            room, "Sorry, something went wrong. Please try again.", True
        )
        bot.logger.log(f"Error adding feed to room {room.room_id}: {e}", "error")
