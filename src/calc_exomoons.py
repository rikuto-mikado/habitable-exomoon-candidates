import pandas as pd
from astropy import units as u
import os


def process_exomoons():
    print("--- Step 1: Loading Raw Data ---")
    input_path = "data/raw/jovian_planets_raw.csv"
    try:
        df = pd.read_csv(input_path)
        print(f"Successfully loaded {len(df)} planets.")
    except FileNotFoundError:
        print(f"Error: {input_path} not found. Please run fetch_nasa.py first.")
        return

    df = df.dropna(
        subset=["pl_orbsmax", "pl_bmassj", "st_mass", "pl_eqt"]
    ).copy()

    print("--- Step 2 & 3: Calculating Hill Radius ---")
    a = df["pl_orbsmax"].values * u.AU
    m_p = df["pl_bmassj"].values * u.Mjup
    m_s = df["st_mass"].values * u.Msun

    mass_ratio = (m_p / (3 * m_s)).decompose()
    hill_radius_au = a * (mass_ratio ** (1 / 3))

    df["hill_radius_AU"] = hill_radius_au.value
    df["hill_radius_km"] = hill_radius_au.to(u.km).value

    print("\n--- Step 4: Filtering for Habitability (Temperature) ---")
    min_temp = 250
    max_temp = 350

    hz_candidates = df[(df["pl_eqt"] >= min_temp) & (df["pl_eqt"] <= max_temp)].copy()
    hz_candidates["est_temp_C"] = hz_candidates["pl_eqt"] - 273.15

    print(
        f"Found {len(hz_candidates)} potential Exomoon host candidates "
        "in the Habitable Zone!"
    )

    print("\n--- Step 5: Formatting and Saving to CSV ---")
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

    final_df = hz_candidates[output_columns].sort_values(
        by="hill_radius_AU", ascending=False
    )

    os.makedirs("data/processed", exist_ok=True)
    output_path = "data/processed/habitable_exomoon_candidates.csv"
    final_df.to_csv(output_path, index=False)

    print(f"Success! Top candidates saved to {output_path}")
    print("\n[Top 5 Habitable Exomoon Candidates (Sorted by Hill Radius)]")
    pd.set_option("display.max_columns", None)
    print(final_df[["pl_name", "est_temp_C", "hill_radius_AU"]].head())


if __name__ == "__main__":
    process_exomoons()
