# bd-labelmaker

Add extra buttons to your BallSpawnView without any code changes.

This will likely not receive any support nor maintenance, but I'll take PRs.

## Installation

Add the following lines to your `config/extra.toml` (create it if it doesn't exist):

```toml
[[ballsdex.packages]]
location = "git+https://github.com/dormieriancitizen/bd-labelmaker.git"
path = "labelmaker_app"
enabled = true

```

## Usage

To use, first add something in the Labels panel, then run `@botping labelmaker_reloadconf` (or use your prefix).

Subsequent spawns will have those buttons added.

Label responses support keywords, such as:

- `{user}` - Mentions the user who interacted with a button.
- `{collectible}` - The collectible name.
- `{collectibles}` - A plural version of `{collectible}`.
- `{ball}` - The countryball's name.
- `{rarity}` - The countryball's rarity.
- `{emoji}` - The countryball's emoji.
- `{discord}` - Your bot's Discord server invite link.

## Example

<img width="905" height="701" alt="image" src="https://github.com/user-attachments/assets/24dc4f2a-9a5a-4509-8e84-3a595aa8199f" />

## Notes

If combined with another app that patches BallSpawnView, one of them will break. This is an essentially unavoidable side effect of allowing hot reloading.
