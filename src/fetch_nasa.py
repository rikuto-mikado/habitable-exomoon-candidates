import requests
import pandas as pd
import io


def fetch_jovian_planets():
    print("Fetching Jovian exoplanet data from NASA Exoplanet Archive...")

    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

    query = """
    SELECT
        pl_name, hostname, pl_orbsmax, pl_bmassj, st_mass, pl_orbeccen, pl_eqt
    FROM
        ps
    WHERE
        default_flag = 1 
        AND pl_bmassj > 0.1 
        AND pl_orbsmax IS NOT NULL 
        AND st_mass IS NOT NULL
    """

    params = {"request": "doQuery", "lang": "ADQL", "query": query, "format": "csv"}
