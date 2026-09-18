# Habitable Exomoon Candidates Hunter

A small Python pipeline for screening giant exoplanets that could host habitable
moons. It downloads confirmed planet data from the NASA Exoplanet Archive,
calculates each planet's Hill radius, and ranks candidates by the size of their
stable gravitational domain.

## How it works

1. `src/fetch_nasa.py` queries the NASA Exoplanet Archive TAP API for planets
   with a mass greater than `0.1 M_Jup` and saves the results to
   `data/raw/jovian_planets_raw.csv`.
2. `src/calc_exomoons.py` uses `astropy` to calculate the Hill radius:

   \[
   R*H = a\left(\frac{M_p}{3M*\*}\right)^{1/3}
   \]

   It then keeps planets with an equilibrium temperature between `250 K` and
   `350 K`, sorts them by Hill radius, and writes
   `data/processed/habitable_exomoon_candidates.csv`.

This is a first-pass screening tool, not a confirmation of exomoon habitability.
Factors such as tidal heating, eclipses, atmospheric composition, and long-term
orbital stability require further analysis.

## Requirements

- Python 3.10+
- Internet access for the NASA Exoplanet Archive query

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the scripts from the repository root:

```bash
python src/fetch_nasa.py
python src/calc_exomoons.py
```

The generated CSV files are stored under `data/raw/` and `data/processed/`.

## License

This project is licensed under the terms in [LICENSE](LICENSE).
