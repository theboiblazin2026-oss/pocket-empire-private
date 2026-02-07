---
name: Web Scraping Pro
description: Beautiful Soup, Selenium, avoiding blocks, and data extraction
---

# Web Scraping Pro Skill

## Tool Selection

| Tool | Best For |
|------|----------|
| requests + BeautifulSoup | Static HTML |
| Selenium | JavaScript-rendered pages |
| Playwright | Modern alternative to Selenium |
| Scrapy | Large-scale crawling |

## Basic Scraping

```python
import requests
from bs4 import BeautifulSoup

response = requests.get('https://example.com')
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements
title = soup.find('h1').text
links = soup.find_all('a', class_='link')
data = soup.select('div.container > p')  # CSS selector
```

## Selenium for Dynamic Pages

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://example.com')

# Wait for element
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'content'))
)

data = element.text
driver.quit()
```

## Avoiding Blocks

| Technique | Implementation |
|-----------|----------------|
| Headers | Set User-Agent, Accept |
| Delays | `time.sleep(random.uniform(1, 3))` |
| Proxies | Rotate IP addresses |
| Sessions | Use requests.Session() |
| Headless | Chrome headless mode |

### Headers Example
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    'Accept': 'text/html,application/xhtml+xml...',
    'Accept-Language': 'en-US,en;q=0.9',
}
response = requests.get(url, headers=headers)
```

## Data Extraction Patterns

```python
# Table to DataFrame
import pandas as pd
table = soup.find('table')
df = pd.read_html(str(table))[0]

# Pagination
for page in range(1, 11):
    url = f'https://example.com/page/{page}'
    # scrape each page
```

## When to Apply
Use when extracting data from websites, automating data collection, or building scrapers.
