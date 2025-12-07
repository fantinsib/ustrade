# ustrade

`ustrade` is a lightweight and easy-to-use Python client for the U.S. Census Bureau
International Trade API. It provides clean functions to retrieve import and export
data, normalize countries and HS codes, and return standardized `pandas` DataFrames.

This library wraps the official Census API endpoints and offers a
simple high-level interface:

```python
import ustrade as ut

df = ut.get_imports("Italy", "1902", "2020-01")
print(df)
