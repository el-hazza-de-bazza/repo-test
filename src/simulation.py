import pandas as pd
from pathlib import Path
import numpy as np

HITRAN_data = pd.read_csv(
    Path(__file__).with_name("CO2Min.csv"),
    usecols=[0, 1, 2],
    header=0,
)
df_HITRAN = pd.DataFrame(HITRAN_data)
wavenumber = np.array(df_HITRAN[df_HITRAN.columns[0]].values.tolist())
print(HITRAN_data.head(1))
print(len(wavenumber)/400)
print(len(wavenumber))
#btw column 1 is wavenumber (in cm^1), then second column is spectral line intensity, nd third is air-broadened HWHM.