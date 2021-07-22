import pandas as pd
import matplotlib.pyplot as plt
plt.close("all")

data = pd.read_csv("snr_data.csv")
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

plt.figure()
plt.xlabel("prediction step")
data.plot()
plt.show()