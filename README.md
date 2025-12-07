# ustrade

> A lightweight and intuitive Python client for the **U.S. Census Bureau International Trade API**.  
Fetch cleanly formatted **imports**, **exports**, **HS codes**, and **country metadata** — all returned as tidy pandas DataFrames.

<p align="left">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/status-active-success" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</p>

---

## 🚀 Features

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

## 📦 Installation

Clone this repository and install via pip in editable mode:

```bash
git clone https://github.com/fantinsib/ustrade.git
cd ustrade
pip install -e .
```
## Quick Example

```python

import ustrade as ust

# Example: Italian imports of pasta and couscous (HS 1902) in January 2020
df = ust.get_imports("FR", "1902", "2020-01")
print(df)
```

## 📘 Full API Reference

### 🔹 `get_imports(country, product, date)`
Fetch monthly import data for a given country and HS code.

**Parameters:**
- `country` — country name (`France`), ISO2 (`FR`), or Census code (`4279`)
- `product` — HS code as string or int (e.g. `2701`)
- `date` — `YYYY-MM` format (e.g. `2020-01`)

**Example:**
```python
ust.get_imports("FR", "10", "2025-01")
```

### 🔹 `get_exports(country, product, date)`
Fetch monthly export data for a given country and HS code.

**Example:**
```python
ust.get_exports("GB", "73", "2019-01")
```

### 🔹 `get_country_by_name(name)`
Look up a country by its full name (case-insensitive).

**Example:**
```python
ust.get_country_by_name("France")
```

### 🔹 `get_country_by_code(code)`
Look up a country using its U.S. Census numeric code.

**Example:**
```python
ust.get_country_by_code("4279")
```

### 🔹 `get_country_by_iso2(iso)`
Look up a country by ISO2 code.

**Example:**
```python
ust.get_country_by_iso2("FR")
```

### 🔹 `get_desc_from_code(hs)`
Return the description associated with an HS code.

**Example:**
```python
ust.get_desc_from_code("2701")
```

---

## 🧩 Notes

- All functions return a **pandas DataFrame** unless otherwise noted.
- Column names are automatically standardized (see schema section).
- `country` inputs can be:
  - `France`
  - `FR`
  - `4279`

  → all resolve to the same internal country object.