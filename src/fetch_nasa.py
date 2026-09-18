import io
import os
import requests
import pandas as pd


def fetch_jovian_planets():
    print("Fetching Jovian exoplanet data from NASA Exoplanet Archive...")

    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

    query = """
    SELECT
        pl_name,
        hostname,
        discoverymethod,
        pl_orbsmax,
        pl_orbeccen,
        pl_orbper,
        pl_bmassj,
        pl_radj,
        pl_eqt,
        pl_insol,
        st_mass,
        st_rad,
        st_teff,
        st_lum,
        st_spectype,
        sy_dist
    FROM
        ps
    WHERE
        default_flag = 1 
        AND pl_bmassj > 0.1 
        AND pl_orbsmax IS NOT NULL 
        AND st_mass IS NOT NULL
    """

    params = {"request": "doQuery", "lang": "ADQL", "query": query, "format": "csv"}

    response = requests.get(url, params=params)

    response.raise_for_status()

    df = pd.read_csv(io.StringIO(response.text))

    # Save data as a CSV file
    from pathlib import Path

    output_dir = Path(__file__).resolve().parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    output_path = raw_dir / "jovian_planets_raw.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Data successfully fetched and saved to {output_path}")
    print(f"Total Jovian planet found: {len(df)}")


if __name__ == "__main__":
    fetch_jovian_planets()
