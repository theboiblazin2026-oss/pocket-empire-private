---
name: Data Visualization
description: Matplotlib, Seaborn, Plotly, chart selection
---

# Data Visualization Skill

## Chart Selection

| Data Type | Best Chart |
|-----------|------------|
| Comparison | Bar chart |
| Trend over time | Line chart |
| Distribution | Histogram, box plot |
| Relationship | Scatter plot |
| Composition | Pie chart, stacked bar |
| Geographic | Map, choropleth |

## Matplotlib

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Sales')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.title('Monthly Sales')
plt.legend()
plt.savefig('chart.png', dpi=300)
plt.show()
```

## Seaborn

```python
import seaborn as sns

# Built-in themes
sns.set_theme(style='whitegrid')

# Charts
sns.barplot(data=df, x='category', y='value')
sns.scatterplot(data=df, x='x', y='y', hue='category')
sns.heatmap(correlation_matrix, annot=True)
sns.boxplot(data=df, x='group', y='value')
```

## Plotly (Interactive)

```python
import plotly.express as px

fig = px.line(df, x='date', y='value', title='Trend')
fig.show()

# Save as HTML
fig.write_html('chart.html')
```

## Best Practices

- Remove chart junk (unnecessary elements)
- Use consistent colors
- Label axes clearly
- Start y-axis at zero (usually)
- Use colorblind-friendly palettes

## When to Apply
Use when creating charts, dashboards, or presenting data insights.
