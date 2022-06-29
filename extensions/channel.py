import logging

from naff import listen, ChannelTypes
from naff.api.events import RawGatewayEvent

from extensions.template import Template

log = logging.getLogger("Sentry")


class ChannelMonitor(Template):
    def __init__(self, bot):
        # noinspection PyProtectedMember
        self.known_types = list(ChannelTypes._value2member_map_.keys())
        self.known_fields = [
            "id",
            "type",
            "guild_id",
            "position",
            "permission_overwrites",
            "name",
            "topic",
            "nsfw",
            "last_message_id",
            "bitrate",
            "user_limit",
            "rate_limit_per_user",
            "recipients",
            "icon",
            "owner_id",
            "application_id",
            "parent_id",
            "last_pin_timestamp",
            "rtc_region",
            "video_quality_mode",
            "message_count",
            "member_count",
            "thread_metadata",
            "member",
            "default_auto_archive_duration",
            "permissions",
            "flags",
        ]

    @listen()
    async def on_raw_channel_create(self, event: RawGatewayEvent):
        await self.dict_parser(event.data)

    @listen()
    async def on_raw_channel_modify(self, event: RawGatewayEvent):
        await self.dict_parser(event.data)

    @listen()
    async def on_raw_channel_delete(self, event: RawGatewayEvent):
        await self.dict_parser(event.data)

    @listen()
    async def on_raw_guild_create(self, event: RawGatewayEvent):
        if "channels" in event.data:
            [await self.dict_parser(channel) for channel in event.data["channels"]]

    async def dict_parser(self, data: dict):

        # noinspection PyProtectedMember
        if not data["type"] in ChannelTypes._value2member_map_:
            if data["type"] not in self.known_types:
                await self.update_types(data["type"])
                log.warning(f"New Channel Type Detected: {data['type']}")

                return await self.bot.report_new_feature(
                    f"New Channel Type Detected", data
                )

        new_fields = [k for k in data if k not in self.known_fields]
        if new_fields:
            await self.update_fields(new_fields)
            log.warning(f"New fields in channels: {new_fields}")

            return await self.bot.report_new_feature(
                f"New fields Detected in Channel Object", data, new_fields=new_fields
            )


def setup(bot):
    ChannelMonitor(bot)
