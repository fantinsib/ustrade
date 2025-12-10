import requests
import socket
from datetime import datetime
import pandas as pd
from urllib.parse import urlencode
from . import countries
from . import codes
from ustrade.codes import HSCode
from ustrade.errors import *

class CensusClient:


    def __init__(self, timeout=10, retries = 3):
        self.timeout = timeout
        self.retries = retries
        self._country_codes = countries._load_countries()
        self._country_by_code = {c.code: c for c in self._country_codes}
        self._country_by_name = {c.name.lower(): c for c in self._country_codes}
        self._country_by_iso  = {c.iso2.upper(): c for c in self._country_codes}

        self.BASE_URL = "api.census.gov"
        self.BASE_PORT = 443

        self._hs_codes, self._codes_by_hs_codes = codes._load_codes()
        self._code_tree = codes.build_tree_from_codes(self._hs_codes)

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
            "MONTH": "month"
        }

        self.type_map = {
            "import_value": "float",
            "export_value": "float",
            "product_name": 'str',
            "product_code": 'str',
            "consumption_import_value": 'float',
            "country": "str",
            "time": "datetime",
            'date': "datetime",
            "country_code": 'str'
        }


        self._cols_to_return = ["date",
                                "country_name",
                                "country_code", 
                                "product_name", 
                                "product_code",
                                "import_value", 
                                "export_value",
                                "consumption_import_value"
                                ]

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
        
                                    ##### DATA RESEARCH FUNCTIONS #######

    def get_imports(self, country : str, product : str, date : str)-> pd.DataFrame:
        """
        Returns the import value from the US to the specified country of the product for the month

        Args:
            country (str | countries.Country) : can be the ISO2 code, the full name, the Census Bureau code for this country, or a Country object
            product (str) : HS code
            date (str): the month, in format 'yyyy-mm'
        """
        return self._get_flow(country, product, date, "imports")
    
    def get_exports(self, country : str, product: str, date: str)-> pd.DataFrame:
        """
        Returns the export value from the US to the specified country of the product for the month

        Args:
            country (str | countries.Country) : can be the ISO2 code, the full name, the Census Bureau code for this country, or a Country object
            product (str) : HS code
            date (str): the month, in format 'yyyy-mm'
        """
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


    def get_imports_on_period(self, country: str, product: str, start: str, end: str)->pd.DataFrame:
        """
        Returns the imports on the specified period
        
        ## Args:
            country (str)
            product (str)
            start (str) : format should be "YYYY-MM"
            end (str): same format
        """
        return self._get_flow_on_period(country, product, start, end, 'imports')
    

    def get_exports_on_period(self, country: str, product: str, start: str, end: str)->pd.DataFrame:
        """
        Returns the imports on the specified period
        
        ## Args:
            country (str)
            product (str)
            start (str) : format should be "YYYY-MM"
            end (str): same format
        """
        return self._get_flow_on_period(country, product, start, end, 'exports')


    def _get_flow_on_period(self, country, product, start, end, flux):
        country = self._normalize_country(country)
        dt_start = datetime.strptime(start, "%Y-%m")
        year_start = dt_start.year
        month_start = f"{dt_start.month:02d}"

        dt_end = datetime.strptime(end, "%Y-%m")
        year_end = dt_end.year
        month_end = f"{dt_end.month:02d}"

        flux_letter = flux[0].upper()

        time_range = f"from+{year_start}-{month_start}+to+{year_end}-{month_end}"

        if flux == 'imports':
            params = {
                "get": f"CTY_CODE,CTY_NAME,{flux_letter}_COMMODITY,{flux_letter}_COMMODITY_SDESC,GEN_VAL_MO,CON_VAL_MO",
                f"{flux_letter}_COMMODITY": str(product),
                "CTY_CODE": str(country)
                
            }

        if flux == "exports":
            params = {
                'get' : f"CTY_CODE,CTY_NAME,{flux_letter}_COMMODITY,{flux_letter}_COMMODITY_SDESC,ALL_VAL_MO",
                f"{flux_letter}_COMMODITY": str(product),
                "CTY_CODE": str(country)
            }

        query = urlencode(params)
        url = f"https://{self.BASE_URL}/data/timeseries/intltrade/{flux}/hs?{query}&time={time_range}"

        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise EmptyResult(
                f"The query '{response.url}' did not return any results."
            )
        header, rows = data[0], data[1:]

        df = pd.DataFrame(rows, columns=header)
        

        return (self._prepare_results_on_period(df))



    def _prepare_results(self, df):
        
        df = df.rename(columns=self.col_mapping)

        df["date"] = (pd.to_datetime(
            df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2))
            .dt.to_period('M')
        )


        
        existing_cols = [c for c in self._cols_to_return if c in df.columns]

        df = df[existing_cols]
        df = df.loc[:, ~df.columns.duplicated()]

        return self._apply_types(df)
        
    def _prepare_results_on_period(self, df):
        df = df.rename(columns= self.col_mapping)
        df["date"] = (
            pd.to_datetime(df["time"], format="%Y-%m", errors="coerce")
            .dt.to_period("M")
        )

        existing_cols = [c for c in self._cols_to_return if c in df.columns]
        df = df[existing_cols]
        df = df.loc[:, ~df.columns.duplicated()]

        return self._apply_types(df)
    


    def _apply_types(self, df):
        for col, t in self.type_map.items():
            if col not in df:
                continue

            if t == "int":
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

            elif t == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)

            elif t == "datetime":
                    df[col] = (
                    df[col].astype(str).str.strip()      
                    .str.replace(r"$", "-01", regex=True)
                    .pipe(pd.to_datetime, errors="coerce")
                    )

            elif t == "str":
                df[col] = df[col].astype(str)

        return df.sort_values(by = "date").reset_index(drop=True)


                                    ####### COUNTRIES FUNCTIONS #######

    def get_country_by_name(self, country: str)-> countries.Country:
        """
        Search a country with its name
        """
        return self._country_by_name[country.lower()]
    
    def get_country_by_code(self, cty_code: str)-> countries.Country:
        """
        Search a country with its code
        """
        return self._country_by_code[cty_code]

    def get_country_by_iso2(self, iso2: str)-> countries.Country:
        """
        Search a country with its ISO 2 ID
        """
        return self._country_by_iso[iso2.upper()]

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
    

                                ####### HS CODES FUNCTIONS #######

    
    def get_desc_from_code(self, hs: str)->str:
        """
        Returns the description of the specified HS code

        ## Args:
            hs (str): the HS code (ex: '1806')
        """
        if isinstance(hs, str):
            if hs in self._codes_by_hs_codes:
                return self._codes_by_hs_codes[hs].description
            else:
                if len(hs) == 1:
                    raise CodeNotFoundError(
                        f"HS code '{hs}' could not be found in the listed codes. Did you mean '0{hs}'?"
                    )
                else:
                    raise CodeNotFoundError(
                        f"HS code '{hs}' could not be found in the listed codes."
                    )
        else:
            raise InvalidCodeError(
                f"Code must be a str instance - received a {type(hs).__name__!r}"
            )
        
    def get_product(self, hs: str) -> HSCode:
        """
        Returns all the informations on a specified HS code through a HSCode object

        ## Args:
            hs (str): the HS code (ex: '1806')
        """
        if isinstance(hs, str):
            if hs in self._codes_by_hs_codes:
                return self._codes_by_hs_codes[hs]
            else:
                if len(hs) == 1:
                    raise CodeNotFoundError(
                        f"HS code '{hs}' could not be found in the listed codes. Did you mean '0{hs}'?"
                    )
                else:
                    raise CodeNotFoundError(
                        f"HS code '{hs}' could not be found in the listed codes."
                    )
                       
        else:
            raise InvalidCodeError(
                f"Code must be a str instance - received a {type(hs).__name__!r}"
            )

    def get_children_codes(self, code: str | HSCode, return_names = True)-> dict | list[str]:
        """
        Returns a dict of the codes and their desc directly attached to code in the hierarchy

        ## Args:
            code (str | HSCode): either the code as a string or the HSCode object
            return_names (bool): returns a dict with the code and the description if true, a list of the codes if false
        
        """
        if isinstance(code, str):
            if code in self._codes_by_hs_codes:
                if return_names:
                    res = {}
                    for p in self.get_product(code)._get_children():
                        res[p] = self.get_desc_from_code(p)
                    return res
                else:
                    return self.get_product(code)._get_children()

            else:
                raise CodeNotFoundError(
                    f"HS code '{code}' could not be found in the listed codes"
                )
        
        elif isinstance(code, HSCode):
            if code in self._codes_by_hs_codes:
                return code._get_children()
            else:
                raise CodeNotFoundError(
                    f"HS code '{code.hscode}' could not be found in the listed codes"
                )
        else:
            raise InvalidCodeError(
                f"Code must be a str or a HSCode instance - received a {type(code).__name__!r}"
            )
        
    




        




