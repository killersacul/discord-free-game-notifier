import calendar
import time
from pathlib import Path

from discord_free_game_notifier.epic import (
    check_promotion,
    game_image,
    game_url,
    promotion_end,
    promotion_start,
)
from discord_free_game_notifier.utils import already_posted

game = {
    "title": "Gloomhaven",
    "id": "9232fdbc352445cc820a54bdc97ed2bb",
    "namespace": "bc079f73f020432fac896d30c8e2c330",
    "description": "Whether you are drawn to Gloomhaven by the call of adventure or by an avid desire for gold glimmering in the dark, your fate will surely be the same. Gloomhaven, the digital adaptation of the acclaimed board game, mixes Tactical-RPG and dungeon-crawling.",
    "effectiveDate": "2022-09-22T15:00:00.000Z",
    "offerType": "BASE_GAME",
    "expiryDate": None,
    "status": "ACTIVE",
    "isCodeRedemptionOnly": False,
    "keyImages": [
        {
            "type": "OfferImageWide",
            "url": "https://cdn1.epicgames.com/spt-assets/ef2777467a3c49059a076e42fd9b41f0/gloomhaven-offer-1j9mc.jpg",
        },
        {
            "type": "OfferImageTall",
            "url": "https://cdn1.epicgames.com/spt-assets/ef2777467a3c49059a076e42fd9b41f0/download-gloomhaven-offer-1ho2x.jpg",
        },
        {
            "type": "Thumbnail",
            "url": "https://cdn1.epicgames.com/spt-assets/ef2777467a3c49059a076e42fd9b41f0/download-gloomhaven-offer-1ho2x.jpg",
        },
    ],
    "seller": {"id": "o-4x4bpaww55p5g3f6xpyqe2cneqxd5d", "name": "Asmodee"},
    "productSlug": None,
    "urlSlug": "0d48da287df14493a7415b560ec1bbb3",
    "url": None,
    "items": [
        {
            "id": "6047532dd78a456593d0ffd6602a7218",
            "namespace": "bc079f73f020432fac896d30c8e2c330",
        }
    ],
    "customAttributes": [
        {"key": "autoGeneratedPrice", "value": "false"},
        {"key": "isManuallySetPCReleaseDate", "value": "true"},
    ],
    "categories": [
        {"path": "freegames"},
        {"path": "games/edition/base"},
        {"path": "games/edition"},
        {"path": "games"},
    ],
    "tags": [
        {"id": "1264"},
        {"id": "1203"},
        {"id": "1367"},
        {"id": "21129"},
        {"id": "1370"},
        {"id": "1386"},
        {"id": "1115"},
        {"id": "21147"},
        {"id": "9547"},
        {"id": "9549"},
    ],
    "catalogNs": {"mappings": [{"pageSlug": "gloomhaven-92f741", "pageType": "productHome"}]},
    "offerMappings": [{"pageSlug": "gloomhaven-92f741", "pageType": "productHome"}],
    "price": {
        "totalPrice": {
            "discountPrice": 0,
            "originalPrice": 3499,
            "voucherDiscount": 0,
            "discount": 3499,
            "currencyCode": "USD",
            "currencyInfo": {"decimals": 2},
            "fmtPrice": {
                "originalPrice": "$34.99",
                "discountPrice": "0",
                "intermediatePrice": "0",
            },
        },
        "lineOffers": [
            {
                "appliedRules": [
                    {
                        "id": "d7d80cbb1f5446f1a051df17c47d2b43",
                        "endDate": "2022-09-29T15:00:00.000Z",
                        "discountSetting": {"discountType": "PERCENTAGE"},
                    }
                ]
            }
        ],
    },
    "promotions": {
        "promotionalOffers": [
            {
                "promotionalOffers": [
                    {
                        "startDate": "2022-09-22T15:00:00.000Z",
                        "endDate": "2022-09-29T15:00:00.000Z",
                        "discountSetting": {
                            "discountType": "PERCENTAGE",
                            "discountPercentage": 0,
                        },
                    }
                ]
            }
        ],
        "upcomingPromotionalOffers": [],
    },
}


def test_promotion_start():
    start_date = None
    if game["promotions"]:
        for promotion in game["promotions"]["promotionalOffers"]:
            for offer in promotion["promotionalOffers"]:
                start_date = calendar.timegm(time.strptime(offer["startDate"], "%Y-%m-%dT%H:%M:%S.%fZ"))

    result = promotion_start(game)
    assert result == start_date


def test_promotion_end():
    end_date = None
    for promotion in game["promotions"]["promotionalOffers"]:
        for offer in promotion["promotionalOffers"]:
            end_date = time.mktime(time.strptime(offer["endDate"], "%Y-%m-%dT%H:%M:%S.%fZ"))

    result = promotion_end(game)
    assert result == end_date


def test_game_image():
    result = game_image(game)
    assert (
            result
            == "https://cdn1.epicgames.com/spt-assets/ef2777467a3c49059a076e42fd9b41f0/download-gloomhaven-offer-1ho2x.jpg"
    )


def test_game_url():
    result = game_url(game)
    assert result == "https://www.epicgames.com/en-US/p/gloomhaven-92f741"


def test_check_promotion():
    assert check_promotion(game)


def test_already_posted():
    file_path = Path("tests/games.txt")
    result = already_posted(file_path, "Half Life 3")
    assert result

    result2 = already_posted(file_path, "Half Life 4")
    assert result2 is False

    result3 = already_posted("Not_a_file", "Sharks")
    assert result3 is False
