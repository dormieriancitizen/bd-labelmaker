from typing import TYPE_CHECKING, cast

from discord import ButtonStyle, Interaction
from discord.ext import commands
from discord.ui import Button

from ballsdex.packages.countryballs.cog import CountryBallsSpawner
import ballsdex.packages.countryballs.cog as countryballs_cog
import ballsdex.packages.countryballs.countryball as countryball
from labelmaker_app.models import Label
from settings.models import settings

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot
    from bd_models.models import Ball


class LabelmakerCog(commands.Cog):
    original: type[countryball.BallSpawnView]

    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    async def cog_load(self):
        self.original = countryball.BallSpawnView
        await self.monkeypatch()

    async def monkeypatch(labelmaker_cog):  # pyright: ignore[reportSelfClsParameterName]
        labels = [label async for label in Label.objects.all()]
        cog = cast("CountryBallsSpawner", labelmaker_cog.bot.get_cog("CountryBallsSpawner"))

        class BallSpawnViewOverride(labelmaker_cog.original):
            def __init__(self, bot: "BallsDexBot", model: "Ball"):
                super().__init__(bot, model)

                for label in labels:

                    async def callback(interaction: Interaction["BallsDexBot"]):
                        await interaction.response.send_message(
                            self.format_response(interaction, label.response), ephemeral=label.ephemeral
                        )

                    style = ButtonStyle(label.style)
                    btn = Button(label=label.label, style=style)
                    btn.callback = callback
                    self.add_item(btn)

            def format_response(self, interaction: Interaction["BallsDexBot"], response: str) -> str:
                return response.format(
                    user=interaction.user.mention,
                    collectibles=settings.plural_collectible_name,
                    collectible=settings.collectible_name,
                    ball=self.model.country,
                    rarity=self.model.rarity,
                    emoji=self.bot.get_emoji(self.model.emoji_id),
                    discord=settings.discord_invite,
                )

            async def on_timeout(self):
                for child in self.children:
                    if isinstance(child, Button):
                        child.disabled = True
                await super().on_timeout()

        cog.countryball_cls = BallSpawnViewOverride
        countryballs_cog.BallSpawnView = BallSpawnViewOverride

    @commands.command()
    @commands.is_owner()
    async def labelmaker_reloadconf(self, ctx: commands.Context["BallsDexBot"]):
        await self.monkeypatch()

        await ctx.reply("Sucessfully reloaded and monkeypatched")
