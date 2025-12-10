####### Test for API calls ######


import ustrade as ut
from ustrade.client import CensusClient




def test_build_client():
    c= CensusClient()


def test_basic_request():
    df = ut.get_exports("Mexico", "27", "2010-01")

    assert len(df) == 1
    assert df.loc[0, "country_name"] == "MEXICO"
    assert df.loc[0, "product_code"] == "27"
    assert df.loc[0, "export_value"] == 773377170.0


def test_get_children_codes():
    children = ut.get_children_codes("1001")

    expected_keys = {"100111", "100119", "100191", "100199"}
    assert set(children.keys()) == expected_keys
    assert "durum wheat" in children["100111"]
