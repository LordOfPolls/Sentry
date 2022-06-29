import logging
import os
import textwrap

import naff
from naff import Client, Activity, ActivityType, Intents, Embed, BrandColours

logging.basicConfig()
log = logging.getLogger("Sentry")
naff_log = logging.getLogger(naff.logger_name)
log.setLevel(logging.DEBUG)
naff_log.setLevel(logging.DEBUG)


class Bot(Client):
    @naff.slash_command("invite", description="Invite Sentry to your server")
    async def cmd_invite(self, ctx: naff.InteractionContext):
        await ctx.send(
            f"https://discord.com/api/oauth2/authorize?client_id={self.app.id}&scope=bot%20applications.commands"
        )

    @naff.listen()
    async def on_startup(self):
        log.info(f"Logged in as {self.user.username}")
        log.info(f"Sentry has been added to {len(self.guilds)} guilds")

    async def report_new_feature(
        self, reason: str, data: dict, new_fields=None, new_type=None
    ):
        channel = await self.fetch_channel(991449742787760208)
        guild = await self.fetch_guild(data.get("guild_id") or data.get("id"))

        embed = Embed(reason.title(), color=BrandColours.BLURPLE)
        embed.footer = f"First Detected in `{guild.name}`"

        description = []

        if new_fields:
            # description is used instead of fields as it allows for more ✨content✨
            description.append("**New Fields**")
            description += [
                f"`{name}`: `{type(data[name]).__name__}` = `{textwrap.shorten(str(data[name] or '[Empty String]'), width=75)}`"
                for name in new_fields
            ]
            # breakpoint()
        if new_type:
            embed.add_field("New Type:", new_type)

        embed.description = "\n".join(description)

        # await channel.send(embed=embed)


if __name__ == "__main__":
    bot = Bot(
        activity=Activity(name="Discord", type=ActivityType.WATCHING),
        intents=Intents.ALL,
        fetch_members=True,
    )
    bot.load_extension("extensions.channel")
    bot.load_extension("extensions.guild")
    bot.load_extension("extensions.member")
    bot.load_extension("extensions.user")
    bot.load_extension("extensions.message")
    bot.start(os.environ["bot_token"])
