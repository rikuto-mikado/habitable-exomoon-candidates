import pandas as pd
import numpy as np
from astropy import units as u
from astropy import constants as const


def process_exomoons():
    # Loading raw data
    input_path = "data/raw/jovian_planets_raw.csv"
    try:
        df = pd.read_csv(input_path)
        print(f"Successfully loaded {len(df)} planets.")
    except FileNotFoundError:
        print(f"Error: {input_path} not found. Please run fetch_nasa.py first.")
        return

    df = df.drop(subset=["pl_orbsmax", "pl_bmassj", "st_mass"]).copy()

    # Applying astropy units
    a = df["pl_orbsmax"].values * u.AU
    m_p = df["pl_bmassj"].values * u.Mjup
    m_s = df["st_mass"].values * u.Msun

    # Calculating Hill Radius
    mass_ratio = (m_p / (3 * m_s)).decompose()
    hill_radius_au = a * (mass_ratio ** (1 / 3))
    df["hill-radius_AU"] = hill_radius_au.value
    df["hill_radius_km"] = hill_radius_au.to(u.km).value

    # For debugging
    print("\n[Preview of calculated Hill Radii]")
    print(df[["pl_name", "pl_orbsmax", "hill_radius_AU"]].head())


if __name__ == "__main__":
    process_exomoons()
