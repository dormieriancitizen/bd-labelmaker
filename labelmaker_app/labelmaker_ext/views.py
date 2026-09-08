from typing import TYPE_CHECKING

from ballsdex.packages.countryballs.countryball import BallSpawnView
from discord import ButtonStyle, Interaction
from discord.ui import Button

from labelmaker_app.models import Label
from settings.models import settings

if TYPE_CHECKING:
    from ballsdex.core.bot import BallsDexBot
    from bd_models.models import Ball


class BallSpawnViewOverride(BallSpawnView):
    labels: list[Label] = []

    def __init__(self, bot: "BallsDexBot", model: "Ball"):
        self.label_map: dict[Button, Label] = {}

        super().__init__(bot, model)

        for label in self.labels:
            async def callback(interaction: Interaction["BallsDexBot"], current_label: Label = label) -> None:
                await interaction.response.send_message(
                    self._format_response(interaction, current_label.response), ephemeral=current_label.ephemeral,
                )

            button = Button(
                label=label.label, style=ButtonStyle(label.style), emoji=label.emoji if label.emoji != "" else None,
            )
            button.callback = callback

            self.label_map[button] = label
            self.catch_row.add_item(button)

    @property
    def caught(self) -> bool:
        return self._caught

    @caught.setter
    def caught(self, value: bool):
        if value:
            for item in self.catch_row.children:
                if isinstance(item, Button):
                    item.disabled = True

            for button, label in self.label_map.items():
                if not label.caught_override:
                    continue

                button.label = label.caught_label
                button.style = ButtonStyle(label.caught_style)
                button.emoji = label.caught_emoji if label.caught_emoji != "" else None

        self._caught = value

    def _format_response(self, interaction: Interaction["BallsDexBot"], response: str) -> str:
        return response.format(
            user=interaction.user.mention,
            collectibles=settings.plural_collectible_name,
            collectible=settings.collectible_name,
            ball=self.model.country,
            rarity=self.model.rarity,
            emoji=str(self.bot.get_emoji(self.model.emoji_id)),
            discord=settings.discord_invite,
        )

    async def on_timeout(self) -> None:
        for child in self.catch_row.children:
            if not isinstance(child, Button):
                continue

            label = self.label_map.get(child)

            if label and label.despawn_override and not (self.caught and label.caught_override):
                child.label = label.despawn_label
                child.style = ButtonStyle(label.despawn_style)
                child.emoji = label.despawn_emoji if label.despawn_emoji != "" else None 
            
            child.disabled = True

        await super().on_timeout()
