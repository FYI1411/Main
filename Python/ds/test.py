import pandas as pd
import numpy as np
from functools import reduce
pd.set_option('display.max_rows', 600)
pd.set_option('display.max_columns', 20)
df1 = pd.read_csv('data.csv')
df2 = pd.read_csv('ir.csv')
df3 = pd.read_csv('m2.csv')
dfs = [df1, df2, df3]
df = reduce(lambda left,right: pd.merge(left,right,on='date'), dfs)
print(df)
