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


if __name__ == "__main__":
    process_exomoons()
