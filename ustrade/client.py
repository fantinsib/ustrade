import requests
import socket
from datetime import datetime
import pandas as pd
from . import countries
from . import codes

class CensusClient:


    class APIError(Exception):
        pass

    def __init__(self, timeout=10, rate_limit =5):
        self.timeout = timeout
        self.rate_limit = rate_limit
        self._country_codes = countries._load_countries()
        self._country_by_code = {c.code: c for c in self._country_codes}
        self._country_by_name = {c.name.lower(): c for c in self._country_codes}
        self._country_by_iso  = {c.iso2.upper(): c for c in self._country_codes}

        self.BASE_URL = "api.census.gov"
        self.BASE_PORT = 443

        self._hs_codes = codes._load_codes()
        self._codes_by_hs_codes = {c.hscode: c for c in self._hs_codes}

        self.col_mapping = {
            
            "CTY_CODE": "country_code",
            'CTY_NAME': "country_name",
            "I_ENDUSE": "product_code",
            "I_COMMODITY": "product_code",
            "E_COMMODITY": "product_code",
            "E_ENDUSE": 'product_code',
            "I_ENDUSE_LDESC" : 'product_name',
            "E_ENDUSE_LDESC" : "product_name",
            "I_COMMODITY_SDESC": "product_name",
            "E_COMMODITY_SDESC": "product_name",
            "GEN_VAL_MO" : "import_value",
            'ALL_VAL_MO': "export_value",
            "CON_VAL_MO": 'consumption_import_value',
            "YEAR": "year",
            "MONTH": "month",


        }

        self._cols_to_return = ["date",
                                "country_name",
                                "country_code", 
                                "product_name", 
                                "product_code",
                                "import_value", 
                                "export_value",
                                "consumption_import_value"]

    def _check_connectivity(self) -> bool:
        """
        Check if connection can be made to the API 
        """
        try:
            with socket.create_connection(
                (self.BASE_URL, self.BASE_PORT),
                timeout=self.timeout
            ):
                return True
        except OSError as e:
            print(e)
            return False

    def get_imports(self, country, product, date):
        return self._get_flow(country, product, date, "imports")
    
    def get_exports(self, country, product, date):
        return self._get_flow(country, product, date, "exports")
    

    def _get_flow(self, country, product, date, flux):

        country = self._normalize_country(country)
        dt = datetime.strptime(date, "%Y-%m")
        year = dt.year
        month = f"{dt.month:02d}"
        flux_letter = flux[0].upper()


        if flux == 'imports':
            params = {
                "get": f"CTY_CODE,CTY_NAME,{flux_letter}_COMMODITY,{flux_letter}_COMMODITY_SDESC,GEN_VAL_MO,CON_VAL_MO",
                f"{flux_letter}_COMMODITY": str(product),
                "CTY_CODE": str(country),
                "YEAR": year,
                "MONTH": month,
            }

        if flux == "exports":
            params = {
                'get' : f"CTY_CODE,CTY_NAME,{flux_letter}_COMMODITY,{flux_letter}_COMMODITY_SDESC,ALL_VAL_MO",
                f"{flux_letter}_COMMODITY": str(product),
                "CTY_CODE": str(country),
                "YEAR": year,
                "MONTH": month
            }

        url = f"https://{self.BASE_URL}/data/timeseries/intltrade/{flux}/hs"

        
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            return pd.DataFrame()
        header, rows = data[0], data[1:]

        df = pd.DataFrame(rows, columns=header)
        

        return (self._prepare_results(df))


    def _prepare_results(self, df):
        
        df = df.rename(columns=self.col_mapping)

        df["date"] = pd.to_datetime(
            df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)
            )


        
        existing_cols = df.columns.intersection(self._cols_to_return)

        df = df[existing_cols]
        df = df.loc[:, ~df.columns.duplicated()]

        return df
        
    #def get_exports_on_period(self, start, end):


    def get_country_by_name(self, country: str):
        """
        Search a country with its name
        """
        return self._country_by_name[country.lower()]
    
    def get_country_by_code(self, cty_code: str):
        """
        Search a country with its code
        """
        return self._country_by_code[cty_code]

    def get_country_by_iso2(self, iso2: str):
        """
        Search a country with its ISO 2 ID
        """
        return self._country_by_iso[iso2.upper()]
    
    def get_desc_from_code(self, hs: str):
        return self._codes_by_hs_codes[str(hs)].description

        
    def _normalize_country(self, inp, output="code"):

        def return_output(country):
            match output:
                case "code": return country.code
                case "name": return country.name
                case "iso2": return country.iso2
                case _:
                    raise ValueError(f"Invalid output type: {output!r}")

        if isinstance(inp, countries.Country):
            return return_output(inp)

        value = str(inp).strip()
        upper = value.upper()
        lower = value.lower()

        if upper in self._country_by_iso:
            country = self._country_by_iso[upper]


        elif lower in self._country_by_name:
            country = self._country_by_name[lower]

        elif value in self._country_by_code:
            country = self._country_by_code[value]

        else:
            raise ValueError(f"Unknown country: {inp!r}")
        
        return return_output(country)





    




        




