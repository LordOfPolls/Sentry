import logging

from naff import listen
from naff.api.events import RawGatewayEvent

from extensions.template import Template

log = logging.getLogger("Sentry")


class MemberMonitor(Template):
    def __init__(self, bot):
        self.known_fields = [
            "user",
            "nick",
            "avatar",
            "guild_avatar",
            "roles",
            "joined_at",
            "premium_since",
            "deaf",
            "mute",
            "pending",
            "permissions",
            "communication_disabled_until",
            "id",
            "guild_id",
            "bot",
            "role_ids",
            "flags",
        ]

    @listen()
    async def on_raw_guild_create(self, event: RawGatewayEvent):
        if "members" in event.data:
            [await self.dict_parser(member) for member in event.data["members"]]

    async def dict_parser(self, data: dict):
        new_fields = [k for k in data if k not in self.known_fields]
        if new_fields:
            await self.update_fields(new_fields)
            log.warning(f"New fields in member: {new_fields}")

            return await self.bot.report_new_feature(
                f"New fields in member", data, new_fields=new_fields
            )


def setup(bot):
    MemberMonitor(bot)
