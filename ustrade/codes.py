from dataclasses import dataclass
from typing import List, Dict, Tuple
import csv
from importlib.resources import files


@dataclass(frozen=True)
class HSCode:
    section: str
    hscode: str
    description: str
    parent: str
    level: int
    children: list

    def _get_children(self) -> list[str]:
        return self.children
    def _get_parent(self) -> str:
        return self.parent


def _load_codes() -> tuple[list[HSCode], dict[str, HSCode], dict[str, HSCode]]:
    csv_path = files(__package__) / "data" / "harmonized-system.csv"
    codes: list[HSCode] = []
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row.pop("Unnamed: 0", None)
            codes.append(
                HSCode(
                    section=row["section"],
                    hscode=row["hscode"],
                    description=row["description"],
                    parent=row["parent"],
                    level=int(row["level"]),
                    children=[],
                )
            )

    return codes, {c.hscode: c for c in codes}, {c.description: c for c in codes}


def _get_parent(code: str) -> str | None:
    code = code.strip()
    if len(code) == 2:
        return None
    elif len(code) == 4:
        return code[:2]
    elif len(code) == 6:
        return code[:4]
    else:
        return None


def build_tree_from_codes(codes: list[HSCode]) -> dict[str, HSCode]:
    """
    Prend une liste de HSCode et remplit `children` pour chaque parent.
    Retourne un dict hscode -> HSCode.
    """
    code_dict: dict[str, HSCode] = {c.hscode: c for c in codes}

    for node in codes:
        parent_code = _get_parent(node.hscode)
        if parent_code is None:
            continue
        if parent_code not in code_dict:
            continue

        parent_node = code_dict[parent_code]
        parent_node.children.append(node.hscode)

    return code_dict
