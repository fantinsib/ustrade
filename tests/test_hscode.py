####### TESTS FOR codes.py ######

import ustrade as ut
from ustrade.codes import HSCode, build_tree_from_codes
import pytest

from ustrade import CensusClient
from ustrade.errors import CodeNotFoundError


def test_build_tree_simple():
    codes = [
        HSCode(section="I", hscode="10", description="Cereals", parent="", level=2, children=[]),
        HSCode(section="I", hscode="1001", description="Wheat", parent="10", level=4, children=[]),
        HSCode(section="I", hscode="100190", description="Other wheat", parent="1001", level=6, children=[]),
    ]

    tree = build_tree_from_codes(codes)

    assert set(tree.keys()) == {"10", "1001", "100190"}
    assert "1001" in tree["10"].children
    assert "100190" in tree["1001"].children
    assert tree["100190"].children == []


def test_build_tree_roots():
    codes = [
        HSCode(section="I", hscode="10", description="Cereals", parent="", level=2, children=[]),
        HSCode(section="I", hscode="1001", description="Wheat", parent="10", level=4, children=[]),
    ]

    tree = build_tree_from_codes(codes)
    roots = [code for code, node in tree.items() if all(code not in n.children for n in tree.values())]
    assert "10" in roots


def test_get_desc_from_code_and_product_roundtrip():
    c = CensusClient()
    desc = c.get_desc_from_code("1001")
    assert isinstance(desc, str)
    assert "wheat" in desc.lower()

    product = c.get_product("1001")
    assert product.hscode == "1001"
    assert product.description == desc


def test_get_desc_from_code_suggests_leading_zero_for_one_digit_code():
    c = CensusClient()
    with pytest.raises(CodeNotFoundError, match="Did you mean '09'\\?"):
        c.get_desc_from_code("9")


def test_get_children_codes_as_list_and_as_object():
    c = CensusClient()
    children_list = c.get_children_codes("1001", return_names=False)
    assert set(children_list) == {"100111", "100119", "100191", "100199"}

    product = c.get_product("1001")
    assert set(c.get_children_codes(product, return_names=False)) == set(children_list)


def test_search_for_code_scoped_and_and_mode():
    c = CensusClient()
    res = c.search_for_code(["durum", "wheat"], mode="AND", in_codes="1001")
    assert "100111" in set(res["Code"])

