import json
import model
import requests
from bs4 import BeautifulSoup
from pyxtension.streams import stream
from .AbstractParser import AbstractParser


class EpicParser(AbstractParser):
    __URL = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=BY" \
          "&allowCountries=BY"

    def parse(self) -> list:
        try:
            response = requests.get(self.__URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            data = json.loads(soup.prettify())
            return stream(data.get('data').get('Catalog').get('searchStore').get('elements')).map(self.__get_game).toList()
        except Exception as e:
            print(e)

    def __get_game(self, elements: dict) -> model.Game:
        dates = self.__get_dates(elements)
        return model.Game(title=elements.get('title'),
                          description=elements.get('description'),
                          original_price=elements.get('price').get('totalPrice').get('fmtPrice').get('originalPrice'),
                          img=self.__find_thumbnail_img(elements.get('keyImages')),
                          from_date=dates.get('startDate'),
                          to_date=dates.get('endDate')
                          )

    def __find_thumbnail_img(self, elements: list) -> str:
        return stream(elements) \
            .filter(lambda element: element.get('type') == 'OfferImageWide') \
            .map(lambda element: element.get('url')) \
            .toList()[0]

    def __get_dates(self, elements: dict) -> dict:
        promotions = elements.get('promotions')
        if promotions is None:
            return {'startDate': '0', 'endDate': '0'}
        elif not promotions.get('upcomingPromotionalOffers'):
            return promotions.get('promotionalOffers')[0].get('promotionalOffers')[0]
        return promotions.get('upcomingPromotionalOffers')[0].get('promotionalOffers')[0]
