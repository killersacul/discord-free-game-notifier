"""Check https://thelovinator1.github.io/discord-free-game-notifier/epic.json for free games.

This is for games that are not found by epic.py.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import requests
from discord_webhook import DiscordEmbed
from loguru import logger

from discord_free_game_notifier import settings
from discord_free_game_notifier.utils import already_posted
from discord_free_game_notifier.webhook import send_embed_webhook

if TYPE_CHECKING:
    from collections.abc import Generator


def create_json_file() -> None:
    """Create or overwrite the Epic.json file with the free games.

    The bot will use this file to check if there are any new free games.
    """
    free_games: dict[str, list[dict[str, str]]] = {
        "free_games": [
            {
                "id": "the_sims_4_my_first_pet_stuff",
                "game_name": "The Sims™ 4 My First Pet Stuff",
                "game_url": "https://store.epicgames.com/en-US/p/the-sims-4--my-first-pet-stuff",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=1,
                    hour=11,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=9,
                    hour=18,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/the_sims_4_my_first_pet_stuff.jpg",
                "description": "Welcome home a new small animal and show love for Cats and Dogs with The Sims™ 4 My First Pet Stuff.\n\n[Instant Checkout](https://store.epicgames.com/purchase?offers=1-2a14cf8a83b149919a2399504e5686a6-7002cdb1eb2543da85ac8a3c4c6d71d5#/)",  # noqa: E501
                "developer": "Maxis",
            },
            {
                "id": "fall_guys_giddy_gift",
                "game_name": "Fall Guys - Giddy Gift",
                "game_url": "https://store.epicgames.com/en-US/p/fall-guys--giddy-gift",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=23,
                    hour=16,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=10,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/fall_guys_giddy_gift.jpg",
                "description": "May we 'present' the free Giddy Gift costume! Wrap up this Winter & earn a crown or two in Fall Guys\n\nIncludes: Giddy Gift (Whole Costume)",  # noqa: E501
                "developer": "Mediatonic",
            },
            {
                "id": "disney_speedstorm_monochromatic_pack",
                "game_name": "Disney Speedstorm - Monochromatic Pack",
                "game_url": "https://store.epicgames.com/en-US/p/disney-speedstorm--monochromatic-pack",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=23,
                    hour=16,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=10,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/disney_speedstorm_monochromatic_pack.jpg",
                "description": "This pack includes:\n• Racing Suit for Goofy: Monochromatic Classic\n• Kart livery for Goofy: Monochromatic Classic\n• Chip n' Dale Rare Crew Shards\n• 5 Universal Box Credits",  # noqa: E501
                "developer": "Gameloft",
            },
            {
                "id": "dark_justiciar_shadowheart_party_pack",
                "game_name": "Dark Justiciar Shadowheart Party Pack",
                "game_url": "https://store.epicgames.com/en-US/p/idle-champions-of-the-forgotten-realms--dark-justiciar-shadow-heart-party-pack",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=23,
                    hour=16,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=10,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/dark_justiciar_shadowheart_party_pack.jpg",
                "description": "This pack unlocks the first 3 Baldur's Gate 3 Champions: Lae'zel, Shadowheart, and Astarion. Also included are 7 Gold Champion Chests for each and an exclusive Skin & Feat Shadowheart!",  # noqa: E501
                "developer": "Codename Entertainment",
            },
            {
                "id": "warframe_holiday_sale_2023",
                "game_name": "Warframe - Holiday Sale 2023",
                "game_url": "https://store.epicgames.com/en-US/p/warframe",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=23,
                    hour=16,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=10,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/warframe_holiday_sale_2023.jpg",
                "description": "Come celebrate the Epic Games Holiday Sale with us and claim the Atterax Weapon, a 7-Day Credit Booster and 7-Day Affinity Booster for free!\nPlayers who launch and log in to WARFRAME on Epic Games Store during the promotional period will receive an inbox message with free content upon login into the game. ",  # noqa: E501
                "developer": "Digital Extremes",
            },
            {
                "id": "honkai_impact_holiday_sale_2023",
                "game_name": "Honkai Impact - Holiday Sale 2023",
                "game_url": "https://store.epicgames.com/en-US/p/honkai-impact-3rd",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=23,
                    hour=16,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=10,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/honkai_impact_holiday_sale_2023.jpg",
                "description": "Celebrate the Epic Games Holiday Sale and get 500 Asterites and 100,000 Coins for free!\nPlayers who log in to Honkai Impact 3rd on Epic Games Store during the event period will receive the bundle via an in-game mail within one week.",  # noqa: E501
                "developer": "miHoYo Limited",
            },
            {
                "id": "synced_holiday_sale_2023",
                "game_name": "SYNCED: Winterfest Bundle",
                "game_url": "https://store.epicgames.com/en-US/p/synced--winterfest-bundle",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=23,
                    hour=16,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=10,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/synced_holiday_sale_2023.jpg",
                "description": "Unlock this Bundle of SYNCED to obtain new Runner and weapon skins, and embrace fresh challenges in the new season - Lambent Dawn.",  # noqa: E501
                "developer": "NExT Studios",
            },
            {
                "id": "world_of_warships_holiday_sale_2023",
                "game_name": "World of Warships — Frosty Celebration Pack",
                "game_url": "https://store.epicgames.com/en-US/p/world-of-warships--frosty-celebration-pack",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=23,
                    hour=16,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=10,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/world_of_warships_holiday_sale_2023.jpg",
                "description": "Embrace the magic of the winter holidays with this free DLC featuring cruiser Ning Hai and the enchanting allure of even more Premium ships that could drop from five festive Santa's Gift containers.",  # noqa: E501
                "developer": "Wargaming",
            },
            {
                "id": "eve_online_superluminal_pack",
                "game_name": "EVE Online - Superluminal Pack",
                "game_url": "https://store.epicgames.com/en-US/p/eve-online--superluminal-pack",
                "start_date": datetime.datetime(
                    year=2023,
                    month=12,
                    day=23,
                    hour=16,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "end_date": datetime.datetime(
                    year=2024,
                    month=1,
                    day=10,
                    hour=0,
                    minute=0,
                    second=0,
                    tzinfo=datetime.UTC,
                ).isoformat(),
                "image_link": "https://thelovinator1.github.io/discord-free-game-notifier/images/eve_online_superluminal_pack.jpg",
                "description": "The Superluminal Pack is a limited-time-only FREE giveaway exclusive to Epic! It contains Semiotique Superluminal SKINs for the Heron, Magnate, Imicus, and Probe as well as unique Superluminal clothing!",  # noqa: E501
                "developer": "CCP Games",
            },
        ],
    }

    with Path.open(Path("pages/epic.json"), "w", encoding="utf-8") as file:
        json.dump(free_games, file, indent=4)
        logger.bind(game_name="Epic").info("Created/updated epic.json")


def get_json() -> dict:
    """Gets a json file from the json folder.

    Returns:
        dict: The json file as a dict.
    """
    json_location: str = "https://thelovinator1.github.io/discord-free-game-notifier/epic.json"
    json_file: dict = {}

    try:
        json_file = requests.get(json_location, timeout=30).json()
    except requests.exceptions.ConnectionError:
        logger.bind(game_name="Epic").error("Unable to connect to github.com")

    logger.bind(game_name="Epic").debug("Got epic.json\n{}", json_file)
    return json_file


def scrape_epic_json() -> Generator[DiscordEmbed, Any, list[Any] | None]:
    """Get the free games from Epic.json.

    Yields:
        Generator[DiscordEmbed, Any, list[Any] | None]: A list of embeds containing the free games.
    """
    # Save previous free games to a file, so we don't post the same games again.
    previous_games: Path = Path(settings.app_dir) / "epic.txt"

    # Create the file if it doesn't exist
    if not Path.exists(previous_games):
        with Path.open(previous_games, "w", encoding="utf-8") as file:
            file.write("")

    # Check Epic.json if free games
    epic_json = get_json()

    # If Epic.json is empty, return an empty list
    if not epic_json:
        return []

    # Get the free games from Epic.json
    free_games = epic_json["free_games"]

    for _game in free_games:
        game_id: str = _game["id"]
        game_name: str = _game["game_name"]
        description: str = _game["description"]
        game_url: str = _game["game_url"]
        image_url: str = _game["image_link"]
        start_date: str = _game["start_date"]
        developer: str = _game["developer"]
        unix_start_date: int = int(
            datetime.datetime.fromisoformat(start_date).timestamp(),
        )
        end_date: str = _game["end_date"]
        unix_end_date: int = int(datetime.datetime.fromisoformat(end_date).timestamp())

        # Check if the game has already been posted
        if already_posted(previous_games, game_id):
            continue

        # Check if the game is still free
        current_time = int(datetime.datetime.now(tz=datetime.UTC).timestamp())
        if unix_end_date < current_time:
            logger.info(f"{game_name} is no longer free")
            continue

        # Create the embed and add it to the list of free games.
        embed = DiscordEmbed(description=description)
        embed.set_author(
            name=f"{game_name}",
            url=game_url,
            icon_url=settings.epic_icon,
        )
        embed.set_image(url=image_url)
        embed.set_timestamp()
        embed.add_embed_field(name="Start", value=f"<t:{unix_start_date}:R>")
        embed.add_embed_field(name="End", value=f"<t:{unix_end_date}:R>")
        embed.set_footer(text=developer)

        with Path.open(previous_games, "a+", encoding="utf-8") as file:
            file.write(f"{game_id}\n")

        yield embed


if __name__ == "__main__":
    create_json_file()
    for game in scrape_epic_json():
        response: requests.Response = send_embed_webhook(game)
        if not response.ok:
            logger.error(
                f"Error when checking game for Epic (JSON):\n{response.status_code} - {response.reason}: {response.text}",  # noqa: E501
            )
