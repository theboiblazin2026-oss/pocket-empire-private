---
name: ETL
description: Extract-Transform-Load pipelines, data cleaning, scheduling
---

# ETL Skill

## Pipeline Structure

```
Extract → Transform → Load
(Source)   (Clean)    (Destination)
```

## Extract

```python
# From API
response = requests.get(api_url)
data = response.json()

# From database
df = pd.read_sql(query, connection)

# From files
df = pd.read_csv('data.csv')
```

## Transform

```python
# Clean missing values
df = df.dropna()
df = df.fillna(0)

# Rename columns
df = df.rename(columns={'old': 'new'})

# Convert types
df['date'] = pd.to_datetime(df['date'])

# Filter
df = df[df['active'] == True]

# Create derived columns
df['total'] = df['price'] * df['quantity']
```

## Load

```python
# To database
df.to_sql('table_name', engine, if_exists='replace')

# To data warehouse
# BigQuery, Snowflake, Redshift, etc.

# To file
df.to_parquet('output.parquet')
```

## Scheduling

| Tool | Best For |
|------|----------|
| cron | Simple Linux scheduling |
| Airflow | Complex DAGs |
| Prefect | Modern Python pipelines |
| dbt | SQL transformations |

## Best Practices

- Idempotent operations (safe to re-run)
- Logging at each step
- Error handling with retries
- Data validation checks
- Incremental loading when possible

## When to Apply
Use when building data pipelines, migrating data, or maintaining data warehouses.
