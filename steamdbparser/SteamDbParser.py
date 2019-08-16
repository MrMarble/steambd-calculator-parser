import json
import logging
import os
import requests
from bs4 import BeautifulSoup


class parser(object):
    def __init__(self):
        self.__headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
        }
        logging.info(
            'New instance of SteamDB Profile Parser has been instanciated'
        )

    def isSteamId(self, steamId):
        """Checks if a string is a valid numeric steam id

        Arguments:
            steamId {string|number} -- Steam ID to check
        """
        return (len(steamId) == 17 and steamId.isdigit())

    def getSteamDBProfile(self, steamId):
        """Returns an object with the information o a Steam Profile.
            {
                "display_name": string,
                "avatar": string,
                "steam_id": string,
                "vanity_url": string,
                "level": string,
                "games": string,
                "games_played": string,
                "price": string,
                "price_lowest": string,
                "price_average": string,
                "price_hour": string,
                "hours": string,
                "hours_average": string,
                "account_age": string,
                "url_steam": string,
                "url_stamdb": string
            }
        Arguments:
            steamId {string} -- Numeric Steam profile ID
        """
        if not self.isSteamId(steamId):
            logging.error(f'{steamId} is not a valid Steam Profile ID')
            raise ValueError

        steamDBUrl = f'https://steamdb.info/calculator/{steamId}'
        profile = {
            "display_name": None,
            "avatar": None,
            "steam_id": steamId,
            "vanity_url": None,
            "level": None,
            "games": None,
            "games_played": None,
            "price": None,
            "price_lowest": None,
            "price_average": None,
            "price_hour": None,
            "hours": None,
            "hours_average": None,
            "account_age": None,
            "url_steam": f'http://steamcommunity.com/profiles/{steamId}',
            "url_stamdb": steamDBUrl
        }
        try:
            logging.info(f'Requesting {steamDBUrl}')
            r = requests.get(
                steamDBUrl, headers=self.__headers, timeout=(3, 10))
            if r.status_code is 200:
                logging.info('Request completed')
                soup = BeautifulSoup(r.text, 'html.parser')

                # Stracting header info first
                header = soup.find('div', 'calculator-wrapper')
                try:
                    avatar = header.select_one('img.avatar')
                    if avatar:
                        profile['avatar'] = avatar['src']
                except Exception:
                    logging.exception('Error getting profile avatar')

                try:
                    display_name = header.select_one('h1.header-title a')
                    if display_name:
                        profile['display_name'] = display_name.contents[0].string
                except Exception:
                    logging.exception('Error getting profile display name')

                try:
                    player_level = header.select_one(
                        'ul.player-info span.friendPlayerLevel')
                    if player_level:
                        profile['level'] = player_level.string
                except Exception:
                    logging.exception('Error getting profile level')

                try:
                    account_age = header.select_one(
                        'ul.player-info > li:nth-child(2) span.number')
                    if account_age:
                        profile['account_age'] = account_age.string
                except Exception:
                    logging.exception('Error getting profile age')

                try:
                    price = header.select_one('div.prices span.number-price')
                    if price:
                        profile['price_lowest'] = price.string # Class name is wrong in steamdb.info
                except Exception:
                    logging.exception('Error getting profile games price')

                try:
                    price_lowest = header.select_one(
                        'div.prices span.number-price-lowest')
                    if price_lowest:
                        profile['price'] = price_lowest.string # Class name is wrong in steamdb.info
                except Exception:
                    logging.exception(
                        'Error getting profile games lowest price')

                try:
                    games = header.select_one(
                        'div.wrapper-info .row-stats .span6:first-child div.progress-desc strong.number')
                    if games:
                        profile['games'] = games.string
                except Exception:
                    logging.exception(
                        'Error getting profile games count')

                try:
                    games_played = header.select_one(
                        'div.wrapper-info .row-stats .span6:first-child div.progress-desc span.number')
                    if games_played:
                        profile['games_played'] = games_played.string
                except Exception:
                    logging.exception(
                        'Error getting profile games played count')
                try:
                    price_average = header.select_one(
                        'div.wrapper-info .row-stats .span3:first-child b')
                    if price_average:
                        profile['price_average'] = price_average.string
                except Exception:
                    logging.exception(
                        'Error getting profile game average price')
                try:
                    price_hour = header.select_one(
                        'div.wrapper-info .row-stats .span3:nth-child(2) b')
                    if price_hour:
                        profile['price_hour'] = price_hour.string
                except Exception:
                    logging.exception(
                        'Error getting profile game price per hour')

                try:
                    hours = header.select_one(
                        'div.wrapper-info .row-stats .span3:nth-child(3) b')
                    if hours:
                        profile['hours'] = hours.string
                except Exception:
                    logging.exception(
                        'Error getting profile hours')
                try:
                    hours_average = header.select_one(
                        'div.wrapper-info .row-stats .span3:nth-child(4) b')
                    if hours_average:
                        profile['hours_average'] = hours_average.string
                except Exception:
                    logging.exception(
                        'Error getting profile average hours')
                try:
                    vanity_url = header.select_one(
                        'div.body-content > .container .tab-content #info > div:first-of-type .span6:first-child table tr:first-child .span2')
                    if vanity_url and vanity_url.string is 'Vanity URL':
                        profile['vanity_url'] = header.select_one(
                            'div.body-content > .container .tab-content #info > div:first-of-type .span6:first-child table tr:first-child a')['href']
                except Exception:
                    logging.exception(
                        'Error getting profile vanity url')
        except Exception:
            logging.exception(
                'Something bad happend when fetching profile info')
        finally:
            return profile
