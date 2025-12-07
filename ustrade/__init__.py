from .countries import Country
from .client import CensusClient

_default_client: CensusClient | None = None

def _get_default_client() -> CensusClient:
    global _default_client
    if _default_client is None:
        _default_client = CensusClient()
    return _default_client

def get_imports(*args, **kwargs):
    """Module-level shortcut: ust.get_imports(...)"""
    return _get_default_client().get_imports(*args, **kwargs)

def get_exports(*args, **kwargs):
    """Module-level shortcut: ust.get_exports(...)"""
    return _get_default_client().get_exports(*args, **kwargs)

def get_country_by_name(country: str):
    """
    Search a country with its name
    """
    return _get_default_client().get_country_by_name(country)

def get_country_by_code(cty_code: str):
    """
    Search a country with its code
    """
    return _get_default_client().get_country_by_code(cty_code)

def get_country_by_iso2(iso2: str):
    """
    Search a country with its ISO 2 ID
    """
    return _get_default_client().get_country_by_iso2(iso2)

def get_desc_from_code(hs: str):
    """
    Returns the description associated with the HS code specified
    """
    return _get_default_client().get_desc_from_code(hs)


__all__ = [
    "CensusClient",
    "Country",
    "get_imports",
    "get_exports",
    "get_country_by_name",
    "get_country_by_code",
    "get_country_by_iso2",
    "get_desc_from_code",
]