# SteamDB Calculator Parser
Simple Python package to parse steamdb.info/calculator/\<steam-id>/

### How to install

You can install this package using pip
`pip install git+https://github.com/MrMarble/steambd-calculator-parser`

### Usage

```python

from steamdbparser import SteamDbParser
steamdb = SteamDbParser.parser()

steamdb.isSteamId('76561198287455504')
>>> True

steamdb.isSteamId('mrmarblet')
>>> False

steamdb.getSteamDBProfile('76561198287455504')
>>> {
        "display_name": "Horus",
        "avatar": "https://steamcdn-a.ak[...]_full.jpg",
        "steam_id": "76561198287455504",
        "vanity_url": "https://steamcommunity.com/id/mrmarblet/",
        "level": "97",
        "games": "1,349",
        "games_played": "943",
        "price": "$10875",
        "price_lowest": "$2796",
        "price_average": "$8.72",
        "price_hour": "$4.36",
        "hours": "4,213h",
        "hours_average": "4.5h",
        "account_age": "3.4", # years
        "url_steam": "https://steamcommunity.com/profiles/76561198287455504",
        "url_stamdb": "https://steamdb.info/calculator/76561198287455504/"
    }
```