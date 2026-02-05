import datetime as dt

import pandas as pd
import pytest
import requests

import ustrade as ut
from ustrade.client import CensusClient
from ustrade.errors import EmptyResult


class FakeResponse:
    def __init__(self, url: str, payload):
        self.url = url
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


@pytest.fixture(autouse=True)
def _reset_default_client():
    ut._default_client = None
    yield
    ut._default_client = None


def test_build_client():
    CensusClient()


def test_get_exports_mocks_api_call(monkeypatch):
    called = {}

    def fake_get(url, timeout):
        called["url"] = url
        payload = [
            [
                "CTY_CODE",
                "CTY_NAME",
                "E_COMMODITY",
                "E_COMMODITY_SDESC",
                "ALL_VAL_MO",
                "YEAR",
                "MONTH",
            ],
            [
                "2010",
                "MEXICO",
                "27",
                "Mineral fuels, oils, distillation products, etc.",
                "773377170",
                "2010",
                "01",
            ],
        ]
        return FakeResponse(url, payload)

    monkeypatch.setattr(requests, "get", fake_get)

    df = ut.get_exports("Mexico", "27", "2010-01")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.loc[0, "country_name"] == "MEXICO"
    assert df.loc[0, "product_code"] == "27"
    assert df.loc[0, "export_value"] == 773377170.0
    assert df.loc[0, "date"].to_pydatetime() == dt.datetime(2010, 1, 1)

    url = called["url"]
    assert url.startswith("https://api.census.gov/data/timeseries/intltrade/exports/hs?")
    assert "CTY_CODE=2010" in url
    assert "E_COMMODITY=27" in url
    assert "YEAR=2010" in url and "MONTH=01" in url


def test_get_imports_mocks_api_call(monkeypatch):
    def fake_get(url, timeout):
        payload = [
            [
                "CTY_CODE",
                "CTY_NAME",
                "I_COMMODITY",
                "I_COMMODITY_SDESC",
                "GEN_VAL_MO",
                "CON_VAL_MO",
                "YEAR",
                "MONTH",
            ],
            [
                "1220",
                "FRANCE",
                "08",
                "Edible fruit and nuts; peel of citrus fruit or melons",
                "123.45",
                "100.0",
                "2018",
                "03",
            ],
        ]
        return FakeResponse(url, payload)

    monkeypatch.setattr(requests, "get", fake_get)

    df = ut.get_imports("France", "08", "2018-03")
    assert len(df) == 1
    assert df.loc[0, "country_name"] == "FRANCE"
    assert df.loc[0, "product_code"] == "08"
    assert df.loc[0, "import_value"] == 123.45
    assert df.loc[0, "consumption_import_value"] == 100.0
    assert df.loc[0, "date"].to_pydatetime() == dt.datetime(2018, 3, 1)


def test_get_exports_returns_empty_df_on_json_decode_error(monkeypatch):
    def fake_get(url, timeout):
        err = requests.exceptions.JSONDecodeError("boom", "", 0)
        return FakeResponse(url, err)

    monkeypatch.setattr(requests, "get", fake_get)

    c = CensusClient()
    df = c.get_exports("Mexico", "27", "2010-01")
    assert df.empty


def test_get_exports_on_period_raises_on_json_decode_error(monkeypatch):
    def fake_get(url, timeout):
        err = requests.exceptions.JSONDecodeError("boom", "", 0)
        return FakeResponse(url, err)

    monkeypatch.setattr(requests, "get", fake_get)

    c = CensusClient()
    with pytest.raises(EmptyResult):
        c.get_exports_on_period("Mexico", "27", "2010-01", "2010-03")


def test_get_children_codes():
    children = ut.get_children_codes("1001")

    expected_keys = {"100111", "100119", "100191", "100199"}
    assert set(children.keys()) == expected_keys
    assert "durum wheat" in children["100111"].lower()
