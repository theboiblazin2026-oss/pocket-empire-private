---
name: NumPy
description: Arrays, broadcasting, linear algebra, performance
---

# NumPy Skill

## Arrays

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.zeros((3, 4))      # 3x4 of zeros
c = np.ones((2, 3))       # 2x3 of ones
d = np.arange(0, 10, 2)   # [0, 2, 4, 6, 8]
e = np.linspace(0, 1, 5)  # 5 evenly spaced
```

## Operations

```python
# Element-wise
a + b          # Addition
a * b          # Multiplication
a ** 2         # Exponentiation

# Matrix
np.dot(a, b)   # Dot product
a @ b          # Same as dot
a.T            # Transpose
```

## Indexing

```python
arr = np.array([[1,2,3], [4,5,6], [7,8,9]])

arr[0]         # First row
arr[:, 1]      # Second column
arr[0:2, 1:3]  # Subarray
arr[arr > 5]   # Boolean mask
```

## Common Functions

```python
np.sum(arr)
np.mean(arr)
np.std(arr)
np.max(arr)
np.argmax(arr)     # Index of max
np.reshape(arr, (3,3))
```

## Performance Tips

- Avoid Python loops over arrays
- Use vectorized operations
- Preallocate arrays instead of append
- Use appropriate dtypes

## When to Apply
Use when doing numerical computing, ML data prep, or scientific computing.
