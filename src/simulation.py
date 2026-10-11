from parameters import x

print("x is:", x)

import pandas as pd
HITRAN_data = pd.read_csv('./CO2Min.csv', usecols=[0,1,2], header=0)
print(HITRAN_data.head(6))