import pandas as pd
import numpy as np
import datetime
from functools import reduce
pd.set_option('display.max_rows', 600)
pd.set_option('display.max_columns', 20)
df1 = pd.read_csv('hpi.csv')
df2 = pd.read_csv('ir.csv')
df3 = pd.read_csv('m2.csv')
df4 = pd.read_csv('gold.csv')
dfs = [df4, df3, df2, df1]
df = reduce(lambda left,right: pd.merge(left,right,on='date'), dfs)
df.to_csv('testdata.csv')
print(df.info())
print(df.describe())
