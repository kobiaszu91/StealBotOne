import requests
import json
from offer import Offer
from bs4 import BeautifulSoup

class AdidasScrapper:
    def __init__(self):
        self._mens_shoes = 'https://www.adidas.pl/pulseboost-hd-ltd-shoes/F33910.html'
        self._mens_cloths = 'https://www.adidas.pl/mezczyzni-ubranie?start='

    def find_steals(self):
        shop_urls = [self._mens_shoes, self._mens_cloths]
        found_steals = []

        for products_url in shop_urls:
            page = 0

            while page<1000:
                print(products_url)
                raw_html = requests.get(products_url).content
                # raw_html = requests.get(products_url+str(page)).content
                # soup_html = BeautifulSoup(raw_html, "html.parser")
                print(raw_html)

                for product_tag in soup_html.find_all('div', {"class": "gl-product-card glass-product-card___1PGiI"}):
                    print(soup_html)
                    if product_tag.find('span', {"class": "gl-price__value gl-price__value--crossed"}):
                        title = product_tag.find('div', {"class": "gl-product-card__name gl-label gl-label--m"}).text
                        old_price = product_tag.find('div', {"class": "gl-price__value gl-price__value--crossed"}).text
                        new_price = product_tag.find('div', {"class": "gl-price__value gl-price__value--sale"}).text
                        url = product_tag.find('a', href=True).attrs['href']
                        url_image = product_tag.find('img', src=True).attrs['src']

                        offer = Offer(title, url, url_image, new_price, old_price)
                        offer.print_offer()
                        found_steals.append(offer)

                page += 48
        return found_steals



