---
name: Python Pro
description: Modern Python best practices for typing, async, packaging, and performance
---

# Python Pro Skill

Apply these patterns when writing or reviewing Python code.

## Type Hints

### Basic Typing
```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def process(items: list[str], count: int = 10) -> dict[str, int]:
    return {item: len(item) for item in items[:count]}
```

### Optional & Union
```python
from typing import Optional

def find_user(id: int) -> Optional[User]:  # Can return None
    ...

# Python 3.10+
def parse(value: str | int) -> str:
    return str(value)
```

### TypedDict & Protocols
```python
from typing import TypedDict, Protocol

class UserDict(TypedDict):
    name: str
    age: int
    email: Optional[str]

class Drawable(Protocol):
    def draw(self) -> None: ...
```

## Async/Await

### Basic Pattern
```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
    )
```

### When to Use Async
| Use Case | Sync or Async? |
|----------|----------------|
| I/O bound (HTTP, DB, files) | ✅ Async |
| CPU bound (calculations) | ❌ Sync (use multiprocessing) |
| Simple scripts | ❌ Sync |

## Project Structure

```
my_project/
├── pyproject.toml      # Modern config (replaces setup.py)
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   └── test_core.py
├── .env
└── README.md
```

### pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
dependencies = ["requests>=2.28"]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]
```

## Best Practices

### Context Managers
```python
# ✅ Always use context managers for resources
with open("file.txt") as f:
    content = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.2f}s")
```

### Dataclasses
```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    email: str
    tags: list[str] = field(default_factory=list)
```

### Error Handling
```python
# ✅ Specific exceptions
try:
    result = process(data)
except ValueError as e:
    logger.warning(f"Invalid data: {e}")
except ConnectionError:
    raise  # Re-raise for caller to handle

# ❌ Avoid bare except
```

## Performance Tips

| Tip | Example |
|-----|---------|
| Use generators for large data | `(x for x in range(1000000))` |
| Use `set` for membership tests | `if x in my_set` vs list |
| Profile before optimizing | `python -m cProfile script.py` |
| Use `__slots__` for many instances | Reduces memory |

## When to Apply
Use when writing Python scripts, APIs, or reviewing Python code.
