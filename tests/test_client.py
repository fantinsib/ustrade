######## Tests for clients core methods ########

from urllib.parse import urlparse, parse_qs
from ustrade import CensusClient


import inspect
from ustrade.client import CensusClient  

def test_debug():
    print("module:", CensusClient.__module__)
    print("file:", inspect.getfile(CensusClient))
    print("_build_params in dir?", "_build_params" in dir(CensusClient))



def test_build_param():

    c = CensusClient()
    print(type(c))
    print(hasattr(c, "_build_params"))
    print(c.__class__)

    url = c._build_params(["Mexico", "Canada"], ["08", "09"], "imports", start="2013-01", end= "2014-01")
    
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    # URL de base
    assert parsed.scheme == "https"
    assert parsed.netloc == "api.census.gov"
    assert "/intltrade/imports/hs" in parsed.path

    # Paramètres critiques
    assert "get" in qs
    assert "CTY_CODE" in qs
    assert "I_COMMODITY" in qs
    assert "time" in qs


