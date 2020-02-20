import pandas as pd

bql = pd.read_csv('bql.csv')
bql = bql[~bql['LYB UN Equity'].isna()]
bql = bql.iloc[1:, 1:]
print(bql.columns)
print(bql.head(10))
for i in range(500):
    bql.iloc[:,i+1] = pd.to_numeric(bql.iloc[:,i+1])

print(bql.dtypes)
corrs = bql.corr(method='pearson')
print(corrs)
