import logging

from naff import listen
from naff.api.events import RawGatewayEvent

from extensions.template import Template

log = logging.getLogger("Sentry")


class UserMonitor(Template):
    def __init__(self, bot):
        self.known_fields = [
            "id",
            "username",
            "discriminator",
            "avatar",
            "bot",
            "system",
            "mfa_enabled",
            "banner",
            "accent_color",
            "locale",
            "verified",
            "email",
            "flags",
            "premium_type",
            "public_flags",
        ]

    @listen()
    async def on_raw_guild_create(self, event: RawGatewayEvent):
        if "members" in event.data:
            [
                await self.dict_parser(member.get("user", {}))
                for member in event.data["members"]
            ]

    @listen()
    async def on_raw_guild_members_chunk(self, event: RawGatewayEvent):
        [
            await self.dict_parser(member.get("user", {}))
            for member in event.data["members"]
        ]

    async def dict_parser(self, data: dict):
        new_fields = [k for k in data if k not in self.known_fields]
        if new_fields:
            await self.update_fields(new_fields)
            log.warning(f"New fields in user: {new_fields}")

            return await self.bot.report_new_feature(
                f"New fields in user", data, new_fields=new_fields
            )


def setup(bot):
    UserMonitor(bot)
