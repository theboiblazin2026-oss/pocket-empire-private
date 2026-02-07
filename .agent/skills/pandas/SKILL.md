---
name: Pandas
description: DataFrames, filtering, groupby, merging, CSV/Excel handling
---

# Pandas Skill

## Loading Data

```python
import pandas as pd

df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')
```

## Basic Operations

```python
df.head()           # First 5 rows
df.info()           # Column types
df.describe()       # Statistics
df.columns          # Column names
df.shape            # (rows, cols)
```

## Filtering

```python
# Single condition
df[df['age'] > 30]

# Multiple conditions
df[(df['age'] > 30) & (df['city'] == 'NYC')]

# Query syntax
df.query('age > 30 and city == "NYC"')
```

## GroupBy

```python
df.groupby('city')['sales'].sum()
df.groupby(['city', 'year']).agg({
    'sales': 'sum',
    'customers': 'count'
})
```

## Merging

```python
# Like SQL JOIN
pd.merge(df1, df2, on='id', how='left')

# Concatenate
pd.concat([df1, df2], ignore_index=True)
```

## Saving

```python
df.to_csv('output.csv', index=False)
df.to_excel('output.xlsx', index=False)
```

## When to Apply
Use when analyzing data, cleaning datasets, or preparing data for ML.
