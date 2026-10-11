from parameters import x

print("x is:", x)

import pandas as pd
from pathlib import Path

HITRAN_data = pd.read_csv(
    Path(__file__).with_name("CO2Min.csv"),
    usecols=[0, 1, 2],
    header=0,
)
print(HITRAN_data.head(6))
#btw column 1 is wavenumber (in cm^1), then second column is spectral line intensity, nd third is air-broadened HWHM.