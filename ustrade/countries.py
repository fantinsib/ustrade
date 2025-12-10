from dataclasses import dataclass
import csv
from importlib.resources import files


@dataclass(frozen=True)
class Country:
    name: str
    code: str
    iso2: str




def _load_countries():
    csv_path = files(__package__) / "data" / "country_codes.csv"


    countries = []
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row.pop("Unnamed: 0", None)
            countries.append(Country(
                name=row["Country"],
                code=row["Code"],
                iso2=row["ISO"],
            ))
    return countries

_COUNTRIES = _load_countries()
_BY_CODE = {c.code: c for c in _COUNTRIES}
_BY_ISO = {c.iso2.upper(): c for c in _COUNTRIES}
_BY_NAME = {c.name.lower(): c for c in _COUNTRIES}

