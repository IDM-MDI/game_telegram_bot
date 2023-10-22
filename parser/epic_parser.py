import json

import requests
from bs4 import BeautifulSoup
from pyxtension.streams import stream
from model.game import Game

url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=BY&allowCountries=BY"


def parse() -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        data = json.loads(soup.prettify())
        return stream(data.get('data').get('Catalog').get('searchStore').get('elements')).map(get_game).toList()
    except Exception as e:
        print(e)


def get_game(elements) -> Game:
    if not isinstance(elements, dict):
        raise ValueError("'elements' param must be dict")

    dates = get_dates(elements)
    return Game(title=elements.get('title'),
                description=elements.get('description'),
                original_price=elements.get('price').get('totalPrice').get('fmtPrice').get('originalPrice'),
                img=find_thumbnail_img(elements.get('keyImages')),
                from_date=dates.get('startDate'),
                to_date=dates.get('endDate')
                )


def find_thumbnail_img(elements) -> str:
    if not isinstance(elements, list):
        raise ValueError("'elements' param must be list")
    return stream(elements) \
        .filter(lambda element: element.get('type') == 'OfferImageWide') \
        .map(lambda element: element.get('url')) \
        .toList()[0]


def get_dates(elements) -> dict:
    if not isinstance(elements, dict):
        raise ValueError("'elements' param must be dict")
    promotions = elements.get('promotions')
    if promotions is None:
        return {'startDate': '0', 'endDate': '0'}
    elif not promotions.get('upcomingPromotionalOffers'):
        return promotions.get('promotionalOffers')[0].get('promotionalOffers')[0]
    return promotions.get('upcomingPromotionalOffers')[0].get('promotionalOffers')[0]

