import pandas as pd
from .countries import Country
from .client import CensusClient
from .codes import HSCode
from .errors import *

_default_client: CensusClient | None = None

def _get_default_client() -> CensusClient:
    global _default_client
    if _default_client is None:
        _default_client = CensusClient()
    return _default_client

def get_imports(country : str| Country | list[str | Country], product : str|list[str], date : str)-> pd.DataFrame:
    """
    Returns the import value from the US to the specified country of the product for the month
    Args:
        country (str | Country | list[str | Country]) : can be the ISO2 code, the full name, the Census Bureau code for this country, or a Country object
        product (str | list[str]) : HS code
        date (str): the month, in format 'YYYY-MM'

    Examples:
    >>> ut.get_imports(["France", "GB"], ["12", "13"], "2018-03")
    >>> ut.get_imports("GB", "12", "2018-03")
    """
    return _get_default_client().get_imports(country = country, product= product, date = date)

def get_exports(country : str| Country | list[str | Country], product : str|list[str], date : str)-> pd.DataFrame:
    """
    Returns the export value from the US to the specified country of the product for the month
    
    Args:
        country (str | Country | list[str | Country]) : can be the ISO2 code, the full name, the Census Bureau code for this country, or a Country object
        product (str | list[str]) : HS code
        date (str): the date, in format 'YYYY-MM'
    Examples:
    >>> ut.get_exports(["France", "GB"], ["08", "09"], "2018-03")
    >>> ut.get_exports("GB", "08", "2018-03")
    """
    return _get_default_client().get_exports(country = country, product= product, date = date)

def get_imports_on_period(country : str| Country | list[str | Country], product : str|list[str], start: str, end: str)->pd.DataFrame:
    """
    Return the imports on the specified period

    Args:
        country (str | Country | list[str | Country]):
            ISO2 code, full name, Census Bureau code, or a Country object.
        product (str | list[str]):
            HS code.
        start (str):
            Starting date in format "YYYY-MM".
        end (str):
            Ending date in format "YYYY-MM".

    Examples:
        >>> ut.get_imports_on_period(["France", "DE", "GB"], ["09", "08", "07"], "2016-01", "2018-01")
        >>> from ustrade import CensusClient
        >>> c = CensusClient(timeout=120)
        >>> c.get_imports_on_period(["France", "DE", "GB"], ["08", "07"], "2016-01", "2018-01")

    Notes:
        - Queries can take time to load.
        - Consider increasing `timeout`.
        - Data is only available from 2010-01.
    """
    return _get_default_client().get_imports_on_period(country, product, start, end)


def get_exports_on_period(country : str| Country | list[str | Country], product : str|list[str], start: str, end: str)->pd.DataFrame:
    """
    Return the exports on the specified period.

    Args:
        country (str | Country | list[str | Country]):
            ISO2 code, full name, Census Bureau code, or a Country object.
        product (str | list[str]):
            HS code(s).
        start (str):
            Start date in format "YYYY-MM".
        end (str):
            End date in format "YYYY-MM".

    Examples:
        >>> ut.get_exports_on_period(["France", "DE", "GB"], ["09", "08", "07"], "2016-01", "2018-01")
        >>> from ustrade import CensusClient
        >>> c = CensusClient(timeout=120)
        >>> c.get_exports_on_period(["France", "DE", "GB"], ["08", "07"], "2016-01", "2018-01")

    Notes:
        - Queries can take time to load.
        - Consider increasing `timeout`.
        - Data is only available from 2010-01.
    """
    return _get_default_client().get_exports_on_period(country, product, start, end)

def get_country_by_name(country: str)-> Country:
    """
    Search a country with its name

    Args:
        country (str) : the full name of the country (ex: 'France')
    """
    return _get_default_client().get_country_by_name(country)

def get_country_by_code(cty_code: str):
    """
    Search a country with its code
    
    Args:
        cty_code (str) : the Census Bureau code of the country  (ex: '4120')
    """
    return _get_default_client().get_country_by_code(cty_code)

def get_country_by_iso2(iso2: str):
    """
    Search a country with its ISO 2 ID

    Args:
        iso2 (str) : the ISO2 code of the country  (ex: 'IT')
    """
    return _get_default_client().get_country_by_iso2(iso2)

def get_desc_from_code(hs: str):
    """
    Returns the description associated with the HS code specified

    Args:
        hs (str): the HS code (ex: '73')
    """
    return _get_default_client().get_desc_from_code(hs)

def get_children_codes(code: str | HSCode, return_names = True)-> dict | list[str]:
    """
    Returns a dict of the codes and their desc directly attached to code in the hierarchy

    Args:
        code (str | HSCode): either the code as a string or the HSCode object
        return_names (bool): returns a dict with the code and the description if true, a list of the codes if false    
    """
    return _get_default_client().get_children_codes(code, return_names)

def get_product(hs: str) -> HSCode:
    """
    Returns all the informations on a specified HS code through a HSCode object

    Args:
        hs (str): the HS code (ex: '1806')
    """
    return _get_default_client().get_product(hs)


__all__ = [
    "CensusClient",
    "Country",
    "get_imports",
    "get_exports",
    "get_imports_on_period",
    "get_exports_on_period",
    "get_country_by_name",
    "get_country_by_code",
    "get_country_by_iso2",
    "get_desc_from_code",
    "get_children_codes", 
    "get_product"
]