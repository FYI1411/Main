import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', 600)
pd.set_option('display.max_columns', 20)
df1 = pd.read_csv('data.csv').set_index('date')
df2 = pd.read_csv('ir.csv').set_index('date')
df3 = df1.merge(df2, left_on='date', right_on='date')
fig = plt.figure()
df1.plot()
plt.show()
fig.savefig('output.png')
