from naff import listen
from naff.api.events import RawGatewayEvent

from extensions.template import Template


class GuildMonitor(Template):
    def __init__(self, bot):
        self.known_fields = [
            "id",
            "name",
            "icon",
            "icon_hash",
            "splash",
            "discovery_splash",
            "owner",
            "owner_id",
            "permissions",
            "region",
            "afk_channel_id",
            "afk_timeout",
            "widget_enabled",
            "widget_channel_id",
            "verification_level",
            "default_message_notifications",
            "explicit_content_filter",
            "roles",
            "emojis",
            "features",
            "mfa_level",
            "application_id",
            "system_channel_id",
            "system_channel_flags",
            "rules_channel_id",
            "max_presences",
            "max_members",
            "vanity_url_code",
            "description",
            "banner",
            "premium_tier",
            "premium_subscription_count",
            "preferred_locale",
            "public_updates_channel_id",
            "max_video_channel_users",
            "approximate_member_count",
            "approximate_presence_count",
            "welcome_screen",
            "nsfw_level",
            "stickers",
            "premium_progress_bar_enabled",
            "joined_at",
            "large",
            "unavailable",
            "member_count",
            "voice_states",
            "members",
            "channels",
            "threads",
            "presences",
            "stage_instances",
            "guild_scheduled_events",
        ]

    @listen()
    async def on_raw_guild_create(self, event: RawGatewayEvent):
        await self.dict_parser(event.data)

    @listen()
    async def on_raw_guild_update(self, event: RawGatewayEvent):
        await self.dict_parser(event.data)

    @listen()
    async def on_raw_guild_delete(self, event: RawGatewayEvent):
        await self.dict_parser(event.data)

    async def dict_parser(self, data: dict):
        new_fields = [k for k in data if k not in self.known_fields]
        if new_fields:
            await self.update_fields(new_fields)
            self.log.warning(f"New fields in guild: {new_fields}")

            return await self.bot.report_new_feature(
                f"New fields detected in guild object", data, new_fields=new_fields
            )


def setup(bot):
    GuildMonitor(bot)
