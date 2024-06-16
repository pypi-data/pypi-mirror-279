import asyncio

from nio import (
    AsyncClient,
    AsyncClientConfig,
    WhoamiResponse,
    DevicesResponse,
    Event,
    Response,
    MatrixRoom,
    Api,
    RoomMessageText,
    RoomSendResponse,
    SyncResponse,
    JoinError,
    RoomLeaveError,
    RoomSendError,
    RoomGetStateError,
)

from typing import Optional, List
from configparser import ConfigParser
from datetime import datetime
from io import BytesIO
from urllib.parse import urlparse

import uuid
import traceback
import json

import aiohttp
from aiohttp_socks import ProxyConnector
import markdown2
import feedparser

from .logging import Logger
from .callbacks import RESPONSE_CALLBACKS, EVENT_CALLBACKS
from .commands import COMMANDS


class RSSBot:
    # Default values
    matrix_client: Optional[AsyncClient] = None
    sync_token: Optional[str] = None
    sync_response: Optional[SyncResponse] = None
    logger: Optional[Logger] = Logger()
    room_ignore_list: List[str] = []  # List of rooms to ignore invites from
    config: ConfigParser = ConfigParser()

    # Properties

    @property
    def sync_token(self) -> Optional[str]:
        if self.sync_response:
            return self.sync_response.next_batch

    @property
    def loop_duration(self) -> int:
        return self.config["RSSBot"].getint("LoopDuration", 300)

    @property
    def allowed_users(self) -> List[str]:
        """List of users allowed to use the bot.

        Returns:
            List[str]: List of user IDs. Defaults to [], which means all users are allowed.
        """
        try:
            return json.loads(self.config["RSSBot"]["AllowedUsers"])
        except Exception:
            return []

    @property
    def event_type(self) -> str:
        """Event type of outgoing messages.

        Returns:
            str: The event type of outgoing messages. Either "text" or "notice".
        """
        return self.config["Matrix"].get("EventType", "notice")

    @property
    def display_name(self) -> str:
        """Display name of the bot user.

        Returns:
            str: The display name of the bot user. Defaults to "RSSBot".
        """
        return self.config["RSSBot"].get("DisplayName", "RSSBot")

    @property
    def default_room_name(self) -> str:
        """Default name of rooms created by the bot.

        Returns:
            str: The default name of rooms created by the bot. Defaults to the display name of the bot.
        """
        return self.config["RSSBot"].get("DefaultRoomName", self.display_name)

    @property
    def debug(self) -> bool:
        """Whether to enable debug logging.

        Returns:
            bool: Whether to enable debug logging. Defaults to False.
        """
        return self.config["RSSBot"].getboolean("Debug", False)

    # User agent to use for HTTP requests
    USER_AGENT = (
        "matrix-rssbot/dev (+https://git.private.coffee/PrivateCoffee/matrix-rssbot)"
    )

    @property
    def proxy(self) -> Optional[str]:
        """Proxy to use for HTTP requests.

        Returns:
            Optional[str]: The proxy to use for HTTP requests. Defaults to None.
        """
        return self.config["RSSBot"].get("Proxy")

    @property
    def proxy_onion_only(self) -> bool:
        """Whether to use the proxy only for .onion URLs.

        Returns:
            bool: Whether to use the proxy only for .onion URLs. Defaults to False.
        """
        return self.config["RSSBot"].getboolean("ProxyOnionOnly", False)

    @classmethod
    def from_config(cls, config: ConfigParser):
        """Create a new RSSBot instance from a config file.

        Args:
            config (ConfigParser): ConfigParser instance with the bot's config.

        Returns:
            RSSBot: The new RSSBot instance.
        """

        # Create a new RSSBot instance
        bot = cls()
        bot.config = config

        # Override default values
        if "RSSBot" in config:
            if "LogLevel" in config["RSSBot"]:
                bot.logger = Logger(config["RSSBot"]["LogLevel"])

        # Set up the Matrix client

        assert "Matrix" in config, "Matrix config not found"

        homeserver = config["Matrix"]["Homeserver"]
        bot.matrix_client = AsyncClient(homeserver)
        bot.matrix_client.access_token = config["Matrix"]["AccessToken"]
        bot.matrix_client.user_id = config["Matrix"].get("UserID")
        bot.matrix_client.device_id = config["Matrix"].get("DeviceID")

        # Return the new RSSBot instance
        return bot

    async def _get_user_id(self) -> str:
        """Get the user ID of the bot from the whoami endpoint.
        Requires an access token to be set up.

        Returns:
            str: The user ID of the bot.
        """

        assert self.matrix_client, "Matrix client not set up"

        user_id = self.matrix_client.user_id

        if not user_id:
            assert self.matrix_client.access_token, "Access token not set up"

            response = await self.matrix_client.whoami()

            if isinstance(response, WhoamiResponse):
                user_id = response.user_id
            else:
                raise Exception(f"Could not get user ID: {response}")

        return user_id

    async def _get_device_id(self) -> str:
        """Guess the device ID of the bot.
        Requires an access token to be set up.

        Returns:
            str: The guessed device ID.
        """

        assert self.matrix_client, "Matrix client not set up"

        device_id = self.matrix_client.device_id

        if not device_id:
            assert self.matrix_client.access_token, "Access token not set up"

            devices = await self.matrix_client.devices()

            if isinstance(devices, DevicesResponse):
                device_id = devices.devices[0].id

        return device_id

    async def process_command(self, room: MatrixRoom, event: RoomMessageText):
        """Process a command. Called from the event_callback() method.
        Delegates to the appropriate command handler.

        Args:
            room (MatrixRoom): The room the command was sent in.
            event (RoomMessageText): The event containing the command.
        """

        self.logger.log(
            f"Received command {event.body} from {event.sender} in room {room.room_id}",
            "debug",
        )

        if event.body.startswith("* "):
            event.body = event.body[2:]

        command = event.body.split()[1] if event.body.split()[1:] else None

        await COMMANDS.get(command, COMMANDS[None])(room, event, self)

    async def _event_callback(self, room: MatrixRoom, event: Event):
        self.logger.log("Received event: " + str(event.event_id), "debug")
        try:
            for eventtype, callback in EVENT_CALLBACKS.items():
                if isinstance(event, eventtype):
                    await callback(room, event, self)
        except Exception as e:
            self.logger.log(
                f"Error in event callback for {event.__class__}: {e}", "error"
            )

            if self.debug:
                await self.send_message(
                    room, f"Error: {e}\n\n```\n{traceback.format_exc()}\n```", True
                )

    def user_is_allowed(self, user_id: str) -> bool:
        """Check if a user is allowed to use the bot.

        Args:
            user_id (str): The user ID to check.

        Returns:
            bool: Whether the user is allowed to use the bot.
        """

        return (
            (
                user_id in self.allowed_users
                or f"*:{user_id.split(':')[1]}" in self.allowed_users
                or f"@*:{user_id.split(':')[1]}" in self.allowed_users
            )
            if self.allowed_users
            else True
        )

    async def event_callback(self, room: MatrixRoom, event: Event):
        """Callback for events.

        Args:
            room (MatrixRoom): The room the event was sent in.
            event (Event): The event.
        """

        if event.sender == self.matrix_client.user_id:
            return

        if not self.user_is_allowed(event.sender):
            if len(room.users) == 2:
                await self.matrix_client.room_send(
                    room.room_id,
                    "m.room.message",
                    {
                        "msgtype": "m.notice",
                        "body": f"You are not allowed to use this bot. Please contact {self.operator} for more information.",
                    },
                )
            return

        asyncio.create_task(self._event_callback(room, event))

    async def _response_callback(self, response: Response):
        for response_type, callback in RESPONSE_CALLBACKS.items():
            if isinstance(response, response_type):
                await callback(response, self)

    async def response_callback(self, response: Response):
        asyncio.create_task(self._response_callback(response))

    async def accept_pending_invites(self):
        """Accept all pending invites."""

        assert self.matrix_client, "Matrix client not set up"

        invites = self.matrix_client.invited_rooms

        for invite in [k for k in invites.keys()]:
            if invite in self.room_ignore_list:
                self.logger.log(
                    f"Ignoring invite to room {invite} (room is in ignore list)",
                    "debug",
                )
                continue

            self.logger.log(f"Accepting invite to room {invite}")

            response = await self.matrix_client.join(invite)

            if isinstance(response, JoinError):
                self.logger.log(
                    f"Error joining room {invite}: {response.message}. Not trying again.",
                    "error",
                )

                leave_response = await self.matrix_client.room_leave(invite)

                if isinstance(leave_response, RoomLeaveError):
                    self.logger.log(
                        f"Error leaving room {invite}: {leave_response.message}",
                        "error",
                    )
                    self.room_ignore_list.append(invite)

            else:
                await self.send_message(
                    invite, "Thank you for inviting me to your room!"
                )

    async def upload_file(
        self,
        file: bytes,
        filename: str = "file",
        mime: str = "application/octet-stream",
    ) -> str:
        """Upload a file to the homeserver.

        Args:
            file (bytes): The file to upload.
            filename (str, optional): The name of the file. Defaults to "file".
            mime (str, optional): The MIME type of the file. Defaults to "application/octet-stream".

        Returns:
            str: The MXC URI of the uploaded file.
        """

        bio = BytesIO(file)
        bio.seek(0)

        response, _ = await self.matrix_client.upload(
            bio, content_type=mime, filename=filename, filesize=len(file)
        )

        return response.content_uri

    async def send_message(
        self,
        room: MatrixRoom | str,
        message: str,
        notice: bool = False,
        msgtype: Optional[str] = None,
    ):
        """Send a message to a room.

        Args:
            room (MatrixRoom): The room to send the message to.
            message (str): The message to send.
            notice (bool): Whether to send the message as a notice. Defaults to False.
        """

        if isinstance(room, str):
            room = self.matrix_client.rooms[room]

        markdowner = markdown2.Markdown(extras=["fenced-code-blocks"])
        formatted_body = markdowner.convert(message)

        msgtype = msgtype if msgtype else "m.notice" if notice else "m.text"

        if not msgtype.startswith("rssbot."):
            msgcontent = {
                "msgtype": msgtype,
                "body": message,
                "format": "org.matrix.custom.html",
                "formatted_body": formatted_body,
            }

        else:
            msgcontent = {
                "msgtype": msgtype,
                "content": message,
            }

        msgtype = "m.room.message"
        content = msgcontent

        method, path, data = Api.room_send(
            self.matrix_client.access_token,
            room.room_id,
            msgtype,
            content,
            uuid.uuid4(),
        )

        response = await self.matrix_client._send(
            RoomSendResponse, method, path, data, (room.room_id,)
        )

        if isinstance(response, RoomSendError):
            self.logger.log(f"Error sending message: {response.message}", "error")

    async def send_state_event(
        self,
        room: MatrixRoom | str,
        event_type: str,
        content: dict,
        state_key: str = "",
    ):
        if isinstance(room, MatrixRoom):
            room = room.room_id

        response = await self.matrix_client.room_put_state(
            room, event_type, content, state_key
        )

        return response

    async def get_state_event(
        self, room: MatrixRoom | str, event_type: str, state_key: Optional[str] = None
    ):
        if isinstance(room, MatrixRoom):
            room = room.room_id

        state = await self.matrix_client.room_get_state(room)

        if isinstance(state, RoomGetStateError):
            self.logger.log(f"Could not get state for room {room}")

        for event in state.events:
            if event["type"] == event_type:
                if state_key is None or event["state_key"] == state_key:
                    return event

    async def get_event_type_for_room(self, room: MatrixRoom) -> str:
        """Returns the event type to use for a room

        Either the default event type or the event type set in the room's state

        Args:
            room (MatrixRoom): The room to get the event type for

        Returns:
            str: The event type to use
        """
        state = await self.get_state_event(room, "rssbot.event_type")
        if state:
            return state["content"]["event_type"]
        return self.event_type

    async def set_event_type_for_room(self, room: MatrixRoom, event_type: str):
        """Sets the event type for a room

        This does not check if the event type is valid

        Args:
            room (MatrixRoom): The room to set the event type for
            event_type (str): The event type to set
        """
        await self.send_state_event(
            room, "rssbot.event_type", {"event_type": event_type}
        )

    async def fetch_feed(self, url: str) -> feedparser.FeedParserDict:
        """Fetch the RSS feed, using Tor SOCKS5 proxy for .onion URLs.

        Args:
            url (str): The URL of the RSS feed.

        Returns:
            feedparser.FeedParserDict: The parsed RSS feed.
        """
        parsed = urlparse(url)
        if self.proxy and (
            not self.proxy_onion_only or parsed.hostname.endswith(".onion")
        ):
            connector = ProxyConnector.from_url(self.proxy)
        else:
            connector = aiohttp.TCPConnector()

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                content = await response.text()
                return feedparser.parse(content)

    async def process_room(self, room):
        self.logger.log(f"Processing room {room}", "debug")

        state = await self.get_state_event(room, "rssbot.feeds")

        if not state:
            feeds = []
        else:
            feeds = state["content"]["feeds"]

        for feed in feeds:
            self.logger.log(f"Processing {feed} in {room.room_id}", "debug")

            feed_state = await self.get_state_event(room, "rssbot.feed_state", feed)

            if feed_state:
                self.logger.log(
                    f"Identified feed timestamp as {feed_state['content']['timestamp']}",
                    "debug",
                )
                timestamp = int(feed_state["content"]["timestamp"])
            else:
                timestamp = 0

            try:
                feed_content = await self.fetch_feed(feed)
                new_timestamp = timestamp
                for entry in feed_content.entries:
                    try:
                        entry_time_info = entry.published_parsed
                    except Exception:
                        entry_time_info = entry.updated_parsed

                    entry_timestamp = int(datetime(*entry_time_info[:6]).timestamp())

                    self.logger.log(f"Entry timestamp identified as {entry_timestamp}")

                    if entry_timestamp > timestamp:
                        entry_message = f"__{feed_content.feed.title}: {entry.title}__\n\n{entry.description}\n\n{entry.link}"
                        await self.send_message(
                            room,
                            entry_message,
                            (await self.get_event_type_for_room(room)) == "notice",
                        )
                        new_timestamp = max(entry_timestamp, new_timestamp)

                await self.send_state_event(
                    room, "rssbot.feed_state", {"timestamp": new_timestamp}, feed
                )
            except Exception as e:
                self.logger.log(f"Error processing feed at {feed}: {e}")
                await self.send_message(
                    room,
                    f"Could not access or parse RSS feed at {feed}. Please ensure that you got the URL right, and that it is actually an RSS feed.",
                    True,
                )

    async def process_rooms(self):
        while True:
            self.logger.log("Starting to process rooms", "debug")

            start_timestamp = datetime.now()

            for room in self.matrix_client.rooms.values():
                try:
                    await self.process_room(room)
                except Exception as e:
                    self.logger.log(
                        f"Something went wrong processing room {room.room_id}: {e}",
                        "error",
                    )

            end_timestamp = datetime.now()

            self.logger.log("Done processing rooms", "debug")

            if (
                time_taken := (end_timestamp - start_timestamp).seconds
            ) < self.loop_duration:
                await asyncio.sleep(self.loop_duration - time_taken)

    async def run(self):
        """Start the bot."""

        # Set up the Matrix client

        assert self.matrix_client, "Matrix client not set up"
        assert self.matrix_client.access_token, "Access token not set up"

        if not self.matrix_client.user_id:
            self.matrix_client.user_id = await self._get_user_id()

        if not self.matrix_client.device_id:
            self.matrix_client.device_id = await self._get_device_id()

        client_config = AsyncClientConfig(
            store_sync_tokens=False, encryption_enabled=False, store=None
        )
        self.matrix_client.config = client_config

        # Run initial sync (includes joining rooms)

        self.logger.log("Running initial sync...", "debug")

        sync = await self.matrix_client.sync(timeout=30000, full_state=True)
        if isinstance(sync, SyncResponse):
            await self.response_callback(sync)
        else:
            self.logger.log(f"Initial sync failed, aborting: {sync}", "critical")
            exit(1)

        # Set up callbacks

        self.logger.log("Setting up callbacks...", "debug")

        self.matrix_client.add_event_callback(self.event_callback, Event)
        self.matrix_client.add_response_callback(self.response_callback, Response)

        # Set custom name

        if self.display_name:
            self.logger.log(f"Setting display name to {self.display_name}", "debug")
            asyncio.create_task(self.matrix_client.set_displayname(self.display_name))

        # Start syncing events
        self.logger.log("Starting sync loop...", "warning")
        sync_task = self.matrix_client.sync_forever(timeout=30000, full_state=True)
        feed_task = self.process_rooms()

        tasks = asyncio.gather(sync_task, feed_task)

        try:
            await tasks
        finally:
            tasks.cancel()
            self.logger.log("Syncing one last time...", "warning")
            await self.matrix_client.sync(timeout=30000, full_state=True)

    def __del__(self):
        """Close the bot."""

        if self.matrix_client:
            asyncio.run(self.matrix_client.close())
