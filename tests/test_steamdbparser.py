import pytest
import string
import random
from steamdbparser import SteamDbParser


def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def test_issteamid():
    steam = SteamDbParser.Parser()

    assert steam.isSteamId(76561198287455504) is True  # My SteamID
    assert steam.isSteamId('76561198287455504') is True

    assert steam.isSteamId(''.join(str(random.randint(0, 9)) for i in range(17))) is True

    assert steam.isSteamId(1) is False
    for i in range(10):
        assert steam.isSteamId(random_string(random.randint(0, 20))) is False

def test_steamdb():
        steam = SteamDbParser.Parser()
        account = steam.getSteamDBProfile(76561198057850335)
        assert type(account) is dict
        for key, value in account.items():
            print(value)
            assert (key == key and value is not None)

def test_canConnect():
    steam = SteamDbParser.Parser()
    canConnect = steam.canConnect()
    assert canConnect is True