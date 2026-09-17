import pandas as pd
import numpy as np
from astropy import units as u
from astropy import constants as const
import os


def process_exomoons():
    # Loading raw data
    input_path = "data/jovian_planets_raw.csv"
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

    # Filtering for Habitability (Temperature)
    min_temp = 250
    max_temp = 350

    hz_candidates = df[(df["pl_eqt"] >= min_temp) & (df["pl_eqt"] <= max_temp)].copy()
    hz_candidates["est_temp_C"] = hz_candidates["pl_eqt"] - 273.15

    print(
        f"Found {len(hz_candidates)} potentional Exomoon host candidates in the Habitable Zone!"
    )

    # Formatting and Saving to CSV
    output_columns = [
        "pl_name",
        "hostname",
        "pl_bmassj",
        "pl_orbsmax",
        "pl_orbeccen",
        "pl_eqt",
        "est_temp_C",
        "hill_radius_AU",
        "hill_radius_km",
    ]

    # For debugging
    print("\n[Preview of calculated Hill Radii]")
    print(df[["pl_name", "pl_orbsmax", "hill_radius_AU"]].head())


if __name__ == "__main__":
    process_exomoons()
