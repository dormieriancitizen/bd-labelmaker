from typing import TYPE_CHECKING, cast

from discord.ext import commands

import ballsdex.packages.countryballs.cog as countryballs_cog
import ballsdex.packages.countryballs.countryball as countryball
from ballsdex.packages.countryballs.cog import CountryBallsSpawner

from ..models import Label
from .views import BallSpawnViewOverride

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot


class LabelmakerCog(commands.Cog):
    original: type[countryball.BallSpawnView]

    def __init__(self, bot: "BallsDexBot"):
        self.bot = bot

    async def cog_load(self):
        self.original = countryball.BallSpawnView
        await self.monkeypatch()

    async def monkeypatch(self):
        labels = [label async for label in Label.objects.filter(enabled=True)]
        cog = cast("CountryBallsSpawner", self.bot.get_cog("CountryBallsSpawner"))

        BallSpawnViewOverride.labels = labels

        cog.countryball_cls = BallSpawnViewOverride
        countryballs_cog.BallSpawnView = BallSpawnViewOverride

    @commands.command()
    @commands.is_owner()
    async def labelmaker_reloadconf(self, ctx: commands.Context["BallsDexBot"]):
        await self.monkeypatch()
        await ctx.reply("Successfully reloaded and monkeypatched")
