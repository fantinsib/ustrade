from urllib.parse import parse_qs, urlparse

import pytest

from ustrade.client import CensusClient


def _parse(url: str):
    parsed = urlparse(url)
    return parsed, parse_qs(parsed.query)


def test_build_params_imports_date_month_year():
    c = CensusClient()
    url = c._build_params(["Mexico", "Canada"], ["08", "09"], "imports", date="2013-01")

    parsed, qs = _parse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "api.census.gov"
    assert parsed.path.endswith("/data/timeseries/intltrade/imports/hs")

    assert "get" in qs
    assert "CTY_CODE" in qs and len(qs["CTY_CODE"]) == 2
    assert "I_COMMODITY" in qs and len(qs["I_COMMODITY"]) == 2
    assert qs["YEAR"] == ["2013"]
    assert qs["MONTH"] == ["01"]
    assert "time" not in qs


def test_build_params_imports_date_range_uses_time():
    c = CensusClient()
    url = c._build_params(["Mexico", "Canada"], ["08", "09"], "imports", start="2013-01", end="2014-01")
    _, qs = _parse(url)

    assert "time" in qs
    assert qs["time"] == ["from 2013-01 to 2014-01"]
    assert "YEAR" not in qs and "MONTH" not in qs


def test_normalize_country_accepts_name_iso_code_and_object():
    c = CensusClient()
    mexico = c.get_country_by_name("Mexico")

    assert c._normalize_country("Mexico") == mexico.code
    assert c._normalize_country("mx") == mexico.code
    assert c._normalize_country(mexico.code) == mexico.code
    assert c._normalize_country(mexico, output="iso2") == "MX"


def test_normalize_country_rejects_unknown_country():
    c = CensusClient()
    with pytest.raises(ValueError):
        c._normalize_country("Neverland")

