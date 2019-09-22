import requests
import json
from offer import Offer

class NikeScrapper:
    def __init__(self):
        self._mens_shoes = 'https://store.nike.com/html-services/gridwallData?country=PL&lang_locale=pl_PL&gridwallPath=mczyni-buty/7puZoi3&pn'
        self._mens_cloths = 'https://store.nike.com/html-services/gridwallData?country=PL&lang_locale=pl_PL&gridwallPath=mczyni-odzie/1mdZ7pu&pn'

    def find_steals(self):
        shop_urls = [self._mens_shoes, self._mens_cloths]
        found_steals = []

        for products_url in shop_urls:
            products_json = json.loads(requests.get(products_url).content)
            page = 1

            while products_json['foundProductResults']:
                for property in products_json['sections']:
                    for item in property['items']:
                        if item['inWallContentCard']:
                            continue
                        try:
                            if item['numberOfColors'] > 1:
                                for color in item['colorways']:
                                    if color['overriddenLocalPrice']:
                                        title = str(item['title'])
                                        title = title.replace("'", "")
                                        title = title.replace(" ", "_")
                                        new_price = int(str(color['localPrice']).split()[0])
                                        old_price = int(str(color['overriddenLocalPrice']).split()[0])
                                        url = str(color['pdpUrl'])
                                        url_image = str(color['imageUrl'])
                                        item_color = str(color['colorDescription'])
                                        offer = Offer(title, url, url_image, new_price, old_price, item_color)
                                        found_steals.append(offer)
                                        # offer.print_offer()
                            elif color['overriddenLocalPrice']:
                                title = str(item['title'])
                                title = title.replace("'", "")
                                title = title.replace(" ", "_")
                                old_price = int(str(color['localPrice']).split()[0])

                                new_price = int(str(color['overriddenLocalPrice']).split()[0])
                                url = str(item['pdpUrl'])
                                url_image = str(item['spriteSheet'])
                                offer = Offer(title, url, url_image, new_price, old_price, item_color)
                                found_steals.append(offer)
                                # offer.print_offer()
                        except:
                            continue

                products_json = json.loads(requests.get(products_url + "=" + str(page)).content)
                page += 1



        # for i in found_steals:
        #     print(i.print_offer())
        return found_steals
