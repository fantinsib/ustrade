# ustrade

> A lightweight and intuitive Python client for the **U.S. Census Bureau International Trade API**.  
> Allows to fetch imports and exports between the US and commercial partners - based on Harmonized System codes (HS)

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/status-active-success" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</p>

---

## Features

- **Simple API**: `ust.get_imports()`, `ust.get_exports()`
- Automatic normalization of country inputs:
  - `"France"`
  - `"FR"` (ISO2)
  - `"4279"` (Census code)
- HS codes lookup + product descriptions
- Standardized DataFrame output with clean column names
- Uses a cached internal client for efficiency
- Zero configuration required

---

## Installation

Clone this repository and install via pip in editable mode:

```bash
git clone https://github.com/fantinsib/ustrade.git
cd ustrade
pip install -e .
```
## Quick Example

```python

import ustrade as ust

# Example: Mexican imports of fruits and nuts between January 2010 and January 2025
df = ust.get_imports_on_period("Mexico", "08", "2010-01", "2025-01")
print(df)
```

## Full API Reference

## *Fetching Data*

### • `get_imports(country, product, date)`
Fetch monthly import data for a given country and HS code.

**Parameters:**
- `country` — country name (`France`), ISO2 (`FR`), Census code (`4279`) or `Country` instance, or a list of the previous
- `product` — HS code as string (e.g. `2701`) or list of string
- `date` — `YYYY-MM` format (e.g. `2020-01`)

**Example:**
```python
ust.get_imports("FR", "10", "2025-01")
ust.get_imports(["France", "GB"], ["12", "13"], "2018-03")
```

---

### • `get_exports(country, product, date)`
Fetch monthly export data for a given country and HS code.

**Example:**
```python
ust.get_exports("GB", "73", "2019-01")
ust.get_exports(["France", "GB"], ["08", "09"], "2018-03")
```

---

### • `get_imports_on_period(country, product, start, end)`
Fetch a DataFrame containing monthly imports for a given country and HS code

**Parameters:**
- `country` — country name (`France`), ISO2 (`FR`), Census code (`4279`) or `Country` instance, or list of the previous
- `product` — HS code as string (e.g. `2701`) or list of string
- `start` and `end` — `YYYY-MM` format (e.g. `2020-01`)

**Example:**
```python
ust.get_imports_on_period("Mexico", "27", "2010-01", "2025-01")
ust.get_imports_on_period(["France", "DE", "GB"], ["09", "08", "07"], "2016-01", "2018-01")
```

---

### • `get_exports_on_period(country, product, start, end)`
Fetch a DataFrame containing monthly exports for a given country and HS code

**Example:**
```python
ust.get_exports_on_period("France", "10", "2020-01", "2023-01")
```

---

## *Exploring Codes*

HS Codes follow a tree hierarchy. 

### • `get_desc_from_code(hs)`
Return the description associated with an HS code.

**Example:**
```python
ust.get_desc_from_code("2701")
```

### • `get_children_codes(code, return_names)`
Return a dictionnary of the codes and descriptions attached to the parent code if return_names is True, and a list of the code if return_names if False.

**Example:**
```python
ust.get_children_codes("10")
```


### • `get_product(hs)`
Return the HSCode instance associated with the hs code specified.

**Example:**
```python
ust.get_product("10")
```

## *Exploring countries*

### • `get_country_by_name(name)`
Look up a country by its full name (case-insensitive).

**Example:**
```python
ust.get_country_by_name("France")
```

### • `get_country_by_code(code)`
Look up a country using its U.S. Census numeric code.

**Example:**
```python
ust.get_country_by_code("4279")
```

### • `get_country_by_iso2(iso)`
Look up a country by ISO2 code.

**Example:**
```python
ust.get_country_by_iso2("FR")
```

---

## 🧩 Notes

- All data retrieval functions return a **pandas DataFrame** unless otherwise noted.
- Column names are automatically standardized (see schema section).
- This library is still in <1.0.0 version and can change. Contributions are always welcome !