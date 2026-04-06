from typing import TYPE_CHECKING, cast

from discord import ButtonStyle, Interaction
from discord.ui import Button, button

from ballsdex.packages.countryballs.cog import CountryBallsSpawner
import ballsdex.packages.countryballs.countryball as countryball

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot
    from bd_models.models import Ball


async def setup(bot: "BallsDexBot"):
    cog = cast("CountryBallsSpawner", bot.get_cog("CountryBallsSpawner"))
    original = cog.countryball_cls

    class BallSpawnViewOverride(original):
        def __init__(self, bot: "BallsDexBot", model: "Ball"):
            super().__init__(bot, model)

        @button(style=ButtonStyle.secondary, label="Help me!")
        async def help_button(self, interaction: Interaction["BallsDexBot"], button: Button):
            await interaction.response.send_message(content=f"The ball is {self.model.country}")

    cog.countryball_cls = BallSpawnViewOverride
