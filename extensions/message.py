from naff import listen, MessageTypes
from naff.api.events import RawGatewayEvent

from extensions.template import Template


class MessageMonitor(Template):
    def __init__(self, bot):
        # noinspection PyProtectedMember
        self.known_types = list(MessageTypes._value2member_map_.keys())
        self.known_fields = [
            "id",
            "channel_id",
            "author",
            "content",
            "timestamp",
            "edited_timestamp",
            "tts",
            "mention_everyone",
            "mentions",
            "mention_roles",
            "mention_channels",
            "attachments",
            "embeds",
            "reactions",
            "nonce",
            "pinned",
            "webhook_id",
            "type",
            "activity",
            "application",
            "application_id",
            "message_reference",
            "flags",
            "referenced_message",
            "interaction",
            "thread",
            "components",
            "sticker_items",
            "stickers",
            "member",
            "guild_id",
        ]

    @listen()
    async def on_raw_message_create(self, event: RawGatewayEvent):
        await self.dict_parser(event.data)

    async def dict_parser(self, data: dict):
        # noinspection PyProtectedMember
        if not data["type"] in MessageTypes._value2member_map_:
            await self.update_types(data["type"])
            self.log.warning(f"New Message Type Detected: {data['type']}")

            return await self.bot.report_new_feature(
                f"New Message Type Detected", data, new_type=data["type"]
            )

        new_fields = [k for k in data if k not in self.known_fields]
        if new_fields:
            await self.update_fields(new_fields)
            self.log.warning(f"New fields in message: {new_fields}")

            return await self.bot.report_new_feature(
                f"New fields in message", data, new_fields=new_fields
            )


def setup(bot):
    MessageMonitor(bot)
