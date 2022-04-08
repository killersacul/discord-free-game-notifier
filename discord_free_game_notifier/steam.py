import os
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from dhooks import Embed

from discord_free_game_notifier import settings

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"  # noqa: E501
STEAM_URL = "https://store.steampowered.com/search/?maxprice=free&specials=1"


def get_free_steam_games() -> List[Embed]:
    """Go to the Steam store and check for free games and return them.

    Returns:
        List[Embed]: List of Embeds containing the free Steam games.
    """
    image_url: str = ""

    # Save previous free games to a file so we don't post the same games again
    previous_games: Path = Path(settings.app_dir) / "steam.txt"
    settings.logger.debug(f"Previous games file: {previous_games}")

    # Create file if it doesn't exist
    if not os.path.exists(previous_games):
        open(previous_games, "w", encoding="utf-8").close()

    # List of dictionaries containing Embeds to send to Discord
    free_games: List[Embed] = []

    request = requests.get(STEAM_URL)
    soup = BeautifulSoup(request.text, "html.parser")

    games = soup.find_all("a", class_="search_result_row")
    for game in games:
        game_name_class = game.find("span", class_="title")
        game_name = game_name_class.text
        settings.logger.debug(f"Game: {game_name}")

        image_url_class = game.find("img", attrs={"src": True})
        image_url = image_url_class["src"]
        settings.logger.debug(f"\tImage: {image_url}")

        game_url = game["href"]
        settings.logger.debug(f"\tURL: {game_url}")

        # Check if the game has already been posted
        if os.path.isfile(previous_games):
            with open(previous_games, "r", encoding="utf-8") as file:
                if game_name in file.read():
                    settings.logger.debug(
                        "\tHas already been posted before. Skipping!",
                    )
                    continue

            embed = Embed(color=0xFFFFFF, timestamp="now")
            embed.set_author(
                name=game_name,
                url=game_url,
                icon_url="https://lovinator.space/Steam_logo.png",
            )

            # Only add the image if it's not empty
            if image_url:
                embed.set_image(image_url)

            # Add the game to the list of free games
            free_games.append(embed)

            # Save the game title to the previous games file so we don't
            # post it again
            with open(previous_games, "a+", encoding="utf-8") as file:
                file.write(f"{game_name}\n")

    return free_games


if __name__ == "__main__":
    get_free_steam_games()
