

from dataclasses import dataclass
import csv
from importlib.resources import files


@dataclass(frozen=True)
class HSCode:
    section: str
    hscode: str
    description: str
    parent: str
    level: int



def _load_codes():
    csv_path = files(__package__) / "data" / "harmonized-system.csv"


    codes = []
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row.pop("Unnamed: 0", None)
            codes.append(HSCode(
                section=row["section"],
                hscode=row["hscode"],
                description=row["description"],
                parent=row["parent"],
                level=int(row["level"]),

            ))
    return codes