from fredapi import Fred
import pandas as pd

def get_cpi_fred(api_key:str):
    fred = Fred(api_key=api_key)
    serie_cpi_usa = fred.get_series('CPIAUCSL')
    serie_cpi_usa = pd.DataFrame(serie_cpi_usa, columns=["ipc_usa"])
    serie_cpi_usa["Año"] = serie_cpi_usa.index.year.astype(str)
    serie_cpi_usa["Mes"] = serie_cpi_usa.index.month.astype(str)
    return serie_cpi_usa