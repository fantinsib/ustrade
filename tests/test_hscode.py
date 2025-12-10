####### TESTS FOR codes.py ######

import ustrade as ut
from ustrade.codes import HSCode, build_tree_from_codes
from ustrade import CensusClient


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


