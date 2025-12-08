import pandas as pd
from .countries import Country
from .client import CensusClient

_default_client: CensusClient | None = None

def _get_default_client() -> CensusClient:
    global _default_client
    if _default_client is None:
        _default_client = CensusClient(timeout=60)
    return _default_client

def get_imports(*args, **kwargs)-> pd.DataFrame:
    """
    Returns the import value from the US to the specified country of the product for the month
    Args:
        country (str | countries.Country) : can be the ISO2 code, the full name, the Census Bureau code for this country, or a Country object
        product (str) : HS code
        date (str): the month, in format 'yyyy-mm'
    """
    return _get_default_client().get_imports(*args, **kwargs)

def get_exports(*args, **kwargs)-> pd.DataFrame:
    """
    Returns the export value from the US to the specified country of the product for the month
    
    Args:
        country (str | countries.Country) : can be the ISO2 code, the full name, the Census Bureau code for this country, or a Country object
        product (str) : HS code
        date (str): the month, in format 'yyyy-mm'
    """
    return _get_default_client().get_exports(*args, **kwargs)

def get_imports_on_period(country: str, product: str, start: str, end: str)->pd.DataFrame:
    """
    Returns the imports on the specified period.
    Args:
        country (str | countries.Country) : can be the ISO2 code, the full name, the Census Bureau code for this country, or a Country object
        product (str) : HS code
        start (str) : format should be "YYYY-MM"
        end (str): same format
    ## Notes:
        Query can take time to load. Don't hesitate to increase *timeout*. Data is only available from 2010-01.
    """
    return _get_default_client().get_imports_on_period(country, product, start, end)


def get_exports_on_period(country: str, product: str, start: str, end: str)->pd.DataFrame:
    """
    Returns the exports on the specified period  
    ## Args:
        country (str | countries.Country) : can be the ISO2 code, the full name, the Census Bureau code for this country, or a Country object
        product (str) : HS code
        start (str) : format should be "YYYY-MM"
        end (str): same format
    ## Notes:
        Query can take time to load. Don't hesitate to increase *timeout*. Data is only available from 2010-01.
    """
    return _get_default_client().get_exports_on_period(country, product, start, end)

def get_country_by_name(country: str)->countries.Country:
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
        cty_code (str) : the Census Bureau code of the country  (ex : '4120')
    """
    return _get_default_client().get_country_by_code(cty_code)

def get_country_by_iso2(iso2: str):
    """
    Search a country with its ISO 2 ID

    Args:
        iso2 (str) : the ISO2 code of the country  (ex : 'IT')
    """
    return _get_default_client().get_country_by_iso2(iso2)

def get_desc_from_code(hs: str):
    """
    Returns the description associated with the HS code specified

    Args:
        hs (str) : HS code (ex : '73')
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